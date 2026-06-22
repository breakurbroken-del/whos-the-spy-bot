class GameSession:

    def __init__(
        self,
        guild_id,
        vc_id,
        text_channel_id,
        host_id
    ):

        self.guild_id = guild_id

        self.vc_id = vc_id

        self.text_channel_id = text_channel_id

        self.host_id = host_id

        # Players

        self.players = []

        self.ready_players = []

        self.eliminated_players = []

        # Roles

        self.spy_id = None

        self.villager_word = None

        self.spy_word = None

        # Voting

        self.votes = {}

        self.voted_players = []

        # Speaking

        self.speaking_queue = []

        self.current_speaker = None

        # Round

        self.round_number = 1

        # State

        self.game_started = False

        self.voting_active = False

        self.speaking_active = False

        # Tasks

        self.voice_task = None

        self.vote_task = None


active_games = {}


def create_session(
    guild_id,
    vc_id,
    text_channel_id,
    host_id
):

    session = GameSession(
        guild_id,
        vc_id,
        text_channel_id,
        host_id
    )

    active_games[vc_id] = session

    return session


def get_session(vc_id):

    return active_games.get(vc_id)


def session_exists(vc_id):

    return vc_id in active_games


def remove_session(vc_id):

    if vc_id in active_games:
        del active_games[vc_id]
