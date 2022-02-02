from core.zone import line

def check_presence(player, players) -> None:
    e = "Player not in players list."
    if player not in players:
        raise Exception(e)


def check_turn(player, players) -> None:
    e = "It is not player's turn."
    check_presence(player, players)
    if not players.index(player) == players.playing:
        raise Exception(e)


def check_playbook(action, player) -> None:
    e = "Action not in player's playbook."
    action_name = action.__class__.__name__
    if action_name not in player.playbook:
        raise Exception(e)


def check_cooldown(action, player, history) -> None:
    e = "Action hasn't cooled down yet."
    action_name = action.__class__.__name__
    h = history.copy()
    h.reverse()
    coolup = 0
    for event in h:
        event_name = event.__class__.__name__
        c1 = event.player == player
        c2 = event_name == "Pass"
        c3 = event_name == action_name
        if c1 and c2: coolup += 1
        if c1 and c3: coolup = 0

    if (coolup - action.cooldown) < 0:
        raise Exception(e)


def check_cost(action, player) -> None:
    e = "Player hasn't enough actions left."
    if action.cost > player.actions[1]:
        raise Exception(e)


def check_range(intent, player, target) -> None:
    e = "Target is outside of range."
    dx = target[0] - player.position[0]
    dy = target[1] - player.position[1]
    if (dx, dy) not in intent.range.zone:
        raise Exception(e)


def check_visibility(intent, player, target, players, board) -> None:
    e = "Target is outside of sight."
    if not intent.visible: return
    sight = line(player.position, target)
    players_positions = [p.position for p in players]
    for position in sight[1:-1]:
        if not board[position].seethrough: raise Exception(e)
        if position in players_positions: raise Exception(e)


def check_walkability(intent, target, board) -> None:
    e = "Target is not accessible."
    if not intent.walkable: return
    if board[target].walkable:
        raise Exception(e)


def check_availability(intent, target, party) -> None:
    e = "Target is not reachable."
    if intent.available is None: return
    players_positions = [p.position for p in party]
    if intent.available == target not in players_positions:
        raise Exception(e)
