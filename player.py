class Player:

    def __init__(self, username=None, password=None, bank_pin=None, is_member=False, is_active=False, world=None, world_filter=None):
        self.username     = username
        self.password     = password
        self.ban_pin      = bank_pin
        self.is_member    = is_member
        self.is_active    = is_active
        self.world        = world
        self.world_filter = world_filter

    def login():
        max_attempt = 20
        # for attempt_n in range(max_attempt):
            
