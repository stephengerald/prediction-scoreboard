from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "prediction_scoreboard.py"
SDK = "v0.2.16"
PROMPT = "Independently resolve one forecasting-league round"
RULES = "Resolve only from the stored official result statement. A requires the statement to establish option A, B requires option B, and contradictory or incomplete evidence is UNRESOLVED."


def deploy(vm, direct_deploy, alice):
    vm.sender = alice
    return direct_deploy(str(CONTRACT), "City Forecast League", RULES, sdk_version=SDK)


def test_forecast_resolution_and_integer_brier_score(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.create_round("Will the fictional river gauge close above 4.0 meters on Friday?", "Yes, above 4.0 meters", "No, 4.0 meters or below")
    direct_vm.sender = direct_bob
    contract.forecast(1, "A", 80)
    direct_vm.sender = direct_alice
    contract.lock_round(1)
    contract.submit_resolution_evidence(1, "The signed Friday bulletin reports the closing gauge at 4.3 meters, which is above the 4.0-meter threshold.")
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "A"}))
    contract.resolve_round(1)
    direct_vm.sender = direct_bob
    contract.claim_round_score(1)
    assert contract.get_player_score("0x" + direct_bob.hex())["total_score"] == 9600
    assert contract.get_forecast(1, "0x" + direct_bob.hex())["score_claimed"] is True
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True


def test_unresolved_round_allows_one_evidence_revision(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.create_round("Which fictional team wins the final?", "Harbor", "Mesa")
    direct_vm.sender = direct_bob
    contract.forecast(1, "B", 70)
    direct_vm.sender = direct_alice
    contract.lock_round(1)
    contract.submit_resolution_evidence(1, "The initial note says the match occurred but omits the winner and final score.")
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "UNRESOLVED"}))
    contract.resolve_round(1)
    contract.replace_unresolved_evidence(1, "The corrected signed result states Mesa defeated Harbor by 3 goals to 1 in the final.")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "B"}))
    contract.resolve_round(1)
    assert contract.get_round(1)["outcome"] == "B"
    assert contract.get_round(1)["evidence_revision_used"] is True


def test_duplicate_forecast_and_bad_resolution_fail_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = deploy(direct_vm, direct_deploy, direct_alice)
    contract.create_round("Will the fictional permit count exceed ten?", "More than ten", "Ten or fewer")
    direct_vm.sender = direct_bob
    contract.forecast(1, "A", 60)
    with direct_vm.expect_revert("one_forecast_per_round"):
        contract.forecast(1, "B", 75)
    direct_vm.sender = direct_alice
    contract.lock_round(1)
    contract.submit_resolution_evidence(1, "The signed registry states twelve permits were issued, which exceeds ten.")
    direct_vm.mock_llm(PROMPT, json.dumps({"outcome": "YES"}))
    with direct_vm.expect_revert("invalid_outcome"):
        contract.resolve_round(1)
    assert contract.get_round(1)["state"] == "READY_TO_RESOLVE"
