import asyncio

from mechanic.strategy import TcpClient
from mechanic.game import Game


class GameServer:

    def __init__(self):
        self.waiting_client = None

    async def connection_handler(self, client_reader, client_writer):
        client = TcpClient(client_reader, client_writer)
        if self.waiting_client is None:
            self.waiting_client = client
            return
        waiting_client, self.waiting_client = self.waiting_client, None
        # game = Game([waiting_client, client], Game.generate_matches(1))
        game = Game([waiting_client, client], ["PillMap,Buggy"])
        print('game started')
        await game.game_loop()
        print('game done')


gs = GameServer()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.start_server(gs.connection_handler, '0.0.0.0', 8000))
try:
    loop.run_forever()
finally:
    loop.close()
