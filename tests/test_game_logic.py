from magic_shop.game_logic import reward_from_score


def test_reward_from_score_boundaries() -> None:
    assert reward_from_score(-10) == 0
    assert reward_from_score(0) == 0
    assert reward_from_score(59) == 0
    assert reward_from_score(60) == 1
    assert reward_from_score(180) == 3
