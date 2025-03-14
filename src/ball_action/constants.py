from src.constants import data_dir, soccernet_dir

ball_action_dir = data_dir / "ball_action"
experiments_dir = ball_action_dir / "experiments"

ball_action_soccernet_dir = soccernet_dir / "spotting-ball-2023"

train_games = [
    "england_efl/2019-2020/2019-10-01 - Leeds United - West Bromwich",
    "england_efl/2019-2020/2019-10-01 - Hull City - Sheffield Wednesday",
    "england_efl/2019-2020/2019-10-01 - Brentford - Bristol City",
    "england_efl/2019-2020/2019-10-01 - Blackburn Rovers - Nottingham Forest",
]
val_games = [
    "england_efl/2019-2020/2019-10-01 - Middlesbrough - Preston North End",
]
test_games = [
    "england_efl/2019-2020/2019-10-01 - Stoke City - Huddersfield Town",
    "england_efl/2019-2020/2019-10-01 - Reading - Fulham",
]
challenge_games = [
    "england_efl/2019-2020/2019-10-02 - Cardiff City - Queens Park Rangers",
    "england_efl/2019-2020/2019-10-01 - Wigan Athletic - Birmingham City",
]

classes = [
    "PASS",
    "DRIVE",
]

num_classes = len(classes)
target2class = {trg: cls for trg, cls in enumerate(classes)}
class2target = {cls: trg for trg, cls in enumerate(classes)}