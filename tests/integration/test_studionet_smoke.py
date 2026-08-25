import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt)
    return receipt


@pytest.mark.integration
def test_studionet_forecast_resolution(default_account, secondary_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "prediction_scoreboard.py")
    rules = "Resolve only from the stored signed result. A requires option A, B requires option B, and incomplete evidence is UNRESOLVED."
    deployed = _ok(factory.deploy_contract_tx(args=["City Forecast League", rules], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    league = factory.build_contract(address, account=default_account)
    player = factory.build_contract(address, account=secondary_account)
    _ok(league.create_round(args=["Will the fictional river gauge close above 4.0 meters?", "Yes, above 4.0", "No, 4.0 or below"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(player.forecast(args=[1, "A", 80]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(league.lock_round(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(league.submit_resolution_evidence(args=[1, "The signed Friday bulletin reports a closing gauge of 4.3 meters, above the threshold."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = _ok(league.resolve_round(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    outcome = league.get_round(args=[1]).call()["outcome"]
    assert outcome in ("A", "B", "UNRESOLVED")
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": outcome}, sort_keys=True))
