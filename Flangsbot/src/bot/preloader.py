import logging

from .config import COGS

log = logging.getLogger(__name__)

class Preload(object):
    def __init__(self) -> None:
        for cog in COGS:
            setattr(self, cog, False)

    def __str__(self) -> str:
        return f'{self.__class__.__name__}'

    def ready_up(self, cog) -> None:
        """ Sets the cog atributte

        This method when is called will set all the cogs to ready state.
        """
        if getattr(self, cog) != True:
            setattr(self, cog, True)
            log.info(f'COG LOADER >>> [{cog}] -> READY')
    
    def all_ready(self) -> bool:
        """Returns the global state of all cogs
        
        This method will return ``True`` if all cogs are ready, False otherwise.
        """
        return all(
            [
                getattr(self, cog) for cog in COGS
            ]
        )
