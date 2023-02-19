from adafruit_shell import Shell

shell = Shell()

def main():
    shell.clear()
    print("""This script downloads and installs
I2S audio support.
""")
    if not shell.is_raspberry_pi():
        shell.bail("Non-Raspberry Pi board detected.")
    pi_model = shell.get_board_model()
    print("{} detected.\n".format(pi_model))
    if pi_model in ("RASPBERRY_PI_ZERO", "RASPBERRY_PI_ZERO_W"):
        pimodel_select = 0
    elif pi_model in ("RASPBERRY_PI_2B", "RASPBERRY_PI_3B", "RASPBERRY_PI_3B_PLUS", "RASPBERRY_PI_3A_PLUS", "RASPBERRY_PI_ZERO_2_W"):
        pimodel_select = 1
    elif pi_model in ("RASPBERRY_PI_4B", "RASPBERRY_PI_CM4", "RASPBERRY_PI_400"):
        pimodel_select = 2
    else:
        shell.bail("Unsupported Pi board detected.")

    auto_load = shell.prompt("Auto load module at boot?")

    print("Installing...")

    # Get needed packages
    shell.run_command("apt-get -y install git raspberrypi-kernel-headers")

    # Build and install the module
    shell.run_command("make clean")
    shell.run_command("make")
    shell.run_command("make install")

    # Setup auto load at boot if selected
    if auto_load:
        shell.write_text_file(
            "/etc/modules-load.d/snd-i2s-audio-osmos.conf",
            "snd-i2s-audio-osmos"
        )
        shell.write_text_file(
            "/etc/modprobe.d/snd-i2s-audio-osmos.conf",
            "options snd-i2s-audio-osmos rpi_platform_generation={}".format(pimodel_select)
        )

    # Enable I2S overlay
    shell.run_command("sed -i -e 's/#dtparam=i2s/dtparam=i2s/g' /boot/config.txt")
    # Disable aux / hdmi audio output
    shell.run_command("sed -i -e 's/dtparam=audio=on/#dtparam=audio=on/g' /boot/config.txt")
    # Add these dtoverlay for speaker output
    shell.run_command("grep -qxF \
        'dtoverlay=googlevoicehat-soundcard' /boot/config.txt || echo 'dtoverlay=googlevoicehat-soundcard' >> /boot/config.txt")
    shell.run_command("grep -qxF \
        'dtoverlay=i2s-mmap' /boot/config.txt || echo 'dtoverlay=i2s-mmap' >> /boot/config.txt")
    
    # Copy asound.conf file to /etc/ 
    shell.run_command("cp asound.conf /etc/asound.conf")
    
    # Done
    print("DONE.\nSettings take effect on next boot.")
    shell.prompt_reboot()

# Main function
if __name__ == "__main__":
    shell.require_root()
    main()
