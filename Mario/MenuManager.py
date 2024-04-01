import pygame as pg



class MenuManager(object):
    """

    That class allows to easily handle game states. Depending on the situation,
    it updates and renders different things. like game menu and locading menu

    """
    def __init__(self, core):

        self.currentGameState = 'Game'

    def update(self, core):
        if self.currentGameState == 'Game':
            core.get_map().update(core)

    def render(self, core):

        
        if self.currentGameState == 'Game':
            core.get_map().render(core)
            

        pg.display.update()

    def start_loading(self):
        pass































#details missed:
# from LoadingMenu import LoadingMenu
# from MainMenu import MainMenu

#update:

""""  if self.currentGameState == 'MainMenu':
            pass

        elif self.currentGameState == 'Loading':
            self.oLoadingMenu.update(core)"""

#-----------------------------------------------------------
#render:

"""if self.currentGameState == 'MainMenu':
            core.get_map().render_map(core)
            self.oMainMenu.render(core)

        elif self.currentGameState == 'Loading':
            self.oLoadingMenu.render(core)"""


# core.get_map().get_ui().render(core)

#-----------------------------------------------------------------


#start_loading
            # # Start to load the level
            # self.currentGameState = 'Loading'
            # self.oLoadingMenu.update_time()
