# Adware

Adware is usually the least harmful type of malware, because it tries to promote some products and force the user to see advertisements in many ways, for example in the web browser every time the user loads a website. Our adware shows three annoying popup windows on the screen promoting various products.

#### Demonstration of behavior

We don't need any specific preparation before an execution of the adware (`./adware.py`). Immediately after the execution we can see three popup windows showing advertisements on our screen. This might be annoying and still relatively fine, but when we press the close button on any popup window, nothing happens and the ad is still shown on the screen.

Creation of basic **adware** is very simple process as it is described below. That's why you should be always cautious when executing uncommon or not trusted files.

#### How does it work

- Firstly, we create our **adware** and pass it arguments from the system. Because we need a proper GUI,
  we are using Python module called [PySide2](https://pypi.org/project/PySide2/). To learn more about GUI programming, see [the guide to GUI programming in Python](https://wiki.qt.io/Qt_for_Python). Our class **Adware** inherits from the **QApplication** and represents main QT application.
  ```python
  adware = Adware(sys.argv)
  ```
- We call the method _show_ads()_, which creates dialog popups and pass the references to these forms to variable in main module `windows`. It is important not to loose reference to those windows, because otherwise they will not be shown on the screen.
  ```python
  windows = adware.show_ads()
  ```
- Our adware has a property **advert_slogans**, which represents a list of ad slogans we want our victim
  to see. For each of those slogans we want to create a unique popup window by calling the method _create_ad_window()_. 
  ```python
  ad_windows = []
  for advert in self.advert_slogans:
      # Create a new ad window.
      ad_window = self.create_ad_window(advert)
  ```
- Because these windows would popup on the same place on the screen and overlap each other, we need to move the created popup windows to random location on the screen. 
  ```python
   # Move this window to random location on screen.
   x_coordinate, y_coordinate = random.randint(1, 800), random.randint(1, 600)
   ad_window.move(x_coordinate, y_coordinate)
  ```
- To create a popup windows, our function _create_ad_window_ creates a new **AdWindow** with the given slogan. To show the window on the screen, we must call the method _show_.
  ```python
  window = AdWindow(ad_slogan=ad_slogan)
  window.show()
  ```
- The popup window called **AdWindow** inherits from **QDialog** and represents independent window with
layout containing only one label showing the ad. However, to make adware more annoying and show ads more aggressively, we set the window to ignore close signal when the victim presses close button. When this happens, the window obtaines information about a new event called **closeEvent**. We will simply ignore any action so the window stays on the screen.
  ``` python
  def closeEvent(self, event):
      event.ignore()
  ```
