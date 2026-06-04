import time
from pca9632_led import PCA9632

I2C_BUS     = 2
LED_ADDRESS = 0x62


def demo_sequence(led: PCA9632) -> None:
    """Cycle through Red -> Green -> Blue -> White -> Off."""
    colours = [
        ("RED",   led.red),
        ("GREEN", led.green),
        ("BLUE",  led.blue),
        ("WHITE", led.white),
    ]
    for name, fn in colours:
        print(f"  -> {name}")
        fn()
        time.sleep(1)

    print("  -> OFF")
    led.off()
    time.sleep(1)


def main() -> None:
    print("Initialising PCA9632 LED controller ...")

    with PCA9632(i2c_bus=I2C_BUS, address=LED_ADDRESS) as led:

        print("\n[Single colours]")
        led.red()
        print("  -> RED")
        time.sleep(1)

        led.green()
        print
        time.sleep(1)

        led.blue()
        print("  -> BLUE")
        time.sleep(1)

        led.white()
        print("  -> WHITE")
        time.sleep(1)

        led.off()
        print("  -> OFF")
        time.sleep(0.5)

        try:
            while True:
                demo_sequence(led)
        except KeyboardInterrupt:
            print("\nStopped by user.")
            led.off()

if __name__ == "__main__":
    main()