from .hoverable import HoverBehavior, HoverButton
from kivy.factory import Factory

Factory.register('HoverBehavior', HoverBehavior)
Factory.register('HoverButton', HoverButton)