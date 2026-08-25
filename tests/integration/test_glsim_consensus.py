from __future__ import annotations
import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Independently resolve one forecasting-league round"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"outcome": "A"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_forecast_scoring():
    owner, player = create_accounts(2)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "prediction_scoreboard.py")
    rules = "Resolve only from the stored signed result. A requires option A, B requires option B, and incomplete evidence is UNRESOLVED."
    deployed = factory.deploy_contract_tx(args=["City Forecast League", rules], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    address = extract_contract_address(deployed)
    league = factory.build_contract(address, account=owner)
    forecaster = factory.build_contract(address, account=player)
    ok(league.create_round(args=["Will the fictional river gauge close above 4.0 meters?", "Yes, above 4.0", "No, 4.0 or below"]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(forecaster.forecast(args=[1, "A", 80]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(league.lock_round(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(league.submit_resolution_evidence(args=[1, "The signed Friday bulletin reports a closing gauge of 4.3 meters, above the threshold."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(league.resolve_round(args=[1]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(forecaster.claim_round_score(args=[1]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert league.get_player_score(args=[player.address]).call()["total_score"] == 9600

