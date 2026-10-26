import unittest
from unittest.mock import patch
from app.domain import DEMO, process
from app.runtime import Store


class AgentTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(":memory:")
        self.env = patch.dict("os.environ", {"MODEL_BACKEND": "local"})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.store.close()

    def run_plan(self, **changes):
        return process(dict(DEMO, **changes), self.store)["run"]

    def test_write_waits_for_approval(self):
        result = self.run_plan()
        self.assertEqual(result["status"], "waiting_approval")
        self.assertEqual(result["spent"], 2)
        self.assertEqual(self.store.connection.execute("SELECT count(*) FROM agent_proposals").fetchone()[0], 0)

    def test_approved_write_is_exactly_once(self):
        run = self.run_plan()
        process({"action": "approve", "tenant": "demo", "id": run["id"], "actor": "reviewer", "reason": "Pedido verificado"}, self.store)
        first = process({"action": "execute", "tenant": "demo", "id": run["id"]}, self.store)["run"]
        second = process({"action": "execute", "tenant": "demo", "id": run["id"]}, self.store)["run"]
        self.assertEqual(first["status"], "completed")
        self.assertEqual(first["spent"], 5)
        self.assertEqual(first["trace"], second["trace"])
        self.assertEqual(self.store.connection.execute("SELECT count(*) FROM agent_proposals").fetchone()[0], 1)

    def test_budget_cannot_reset_on_resume(self):
        run = self.run_plan(budget=1)
        self.assertEqual(run["status"], "budget_exhausted")
        again = process({"action": "execute", "tenant": "demo", "id": run["id"], "budget": 30}, self.store)["run"]
        self.assertEqual(again["spent"], 1)
        self.assertEqual(len(again["trace"]), 1)

    def test_read_only_plan_finishes(self):
        result = self.run_plan(task="Revisa ORDER-1001")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["trace"][1]["result"]["available"], 12)

    def test_shell_tool_rejected(self):
        with self.assertRaises(ValueError):
            self.run_plan(plan=[{"tool": "shell", "arguments": {"command": "whoami"}}])

    def test_extra_tool_arguments_rejected(self):
        with self.assertRaises(ValueError):
            self.run_plan(plan=[{"tool": "order.lookup", "arguments": {"order_id": "ORDER-1001", "tenant": "other"}}])

    def test_only_one_final_write_allowed(self):
        with self.assertRaises(ValueError):
            self.run_plan(plan=[{"tool": "proposal.create", "arguments": {"order_id": "ORDER-1001"}}, {"tool": "stock.lookup", "arguments": {"sku": "SKU-AX12"}}])

    def test_cross_tenant_run_hidden(self):
        run = self.run_plan()
        with self.assertRaises(ValueError):
            process({"action": "get", "tenant": "other", "id": run["id"]}, self.store)

    def test_rejection_prevents_write(self):
        run = self.run_plan()
        process({"action": "reject", "tenant": "demo", "id": run["id"], "actor": "reviewer", "reason": "No autorizado"}, self.store)
        result = process({"action": "execute", "tenant": "demo", "id": run["id"]}, self.store)["run"]
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(len(result["trace"]), 2)

    def test_stock_rechecked_before_proposal(self):
        run = self.run_plan(task="Propuesta ORDER-1002")
        process({"action": "approve", "tenant": "demo", "id": run["id"], "actor": "reviewer", "reason": "Revisar disponibilidad"}, self.store)
        result = process({"action": "execute", "tenant": "demo", "id": run["id"]}, self.store)["run"]
        self.assertFalse(result["trace"][-1]["result"]["created"])
        self.assertEqual(result["trace"][-1]["result"]["reason"], "insufficient_stock")

    def test_plan_length_and_boolean_budget_rejected(self):
        with self.assertRaises(ValueError):
            self.run_plan(plan=[{"tool": "order.lookup", "arguments": {"order_id": "ORDER-1001"}}] * 7)
        with self.assertRaises(ValueError):
            self.run_plan(budget=True)

    def test_model_plan_cannot_bypass_allowlist(self):
        with patch.dict("os.environ", {"MODEL_BACKEND": "ollama"}), patch("app.providers.structured", return_value={"steps": [{"tool": "http.request", "arguments": {"url": "http://metadata/"}}]}):
            with self.assertRaises(ValueError):
                self.run_plan()
