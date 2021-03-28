import pydirectinput as pdi
import time


class TimingBot():
    def main(self) -> None:
        pdi.FAILSAFE = True

        print("Starting in 5 sec")
        time.sleep(5)

        # Trial press key down
        pdi.keyDown("left")
        time.sleep(1)
        pdi.keyUp("left")

        print("Done")

        pdi.press("esc")
        print("Pressed escape")


tb = TimingBot()
tb.main()
