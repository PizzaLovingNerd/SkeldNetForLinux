# SkeldNetForLinux

This is a tool for Linux that allows you to play Among Us with [skeld.net](https://skeld.net/) modded servers.

![Pic of SkeldNetForLinux](https://i.imgur.com/SM2616C.png)

## Known issues
- "Launch Among Us" option doesn't just launches Steam's Among Us page, and not Among Us
- Doesn't detect if the game isn't installed
- UI isn't very good

# How to install
If this becomes popular enough I will make a .deb and .rpm, however for now just download and run the main.py after installing the dependencies

# Dependencies
`Fedora: dnf install python3 python3-gobject python3-psutil gtk3`

`Debian/Ubuntu: apt install python3 python3-gi gir1.2-gtk-3.0 python3-psutil`

`Arch/Manjaro: pacman -S python python-gobject gtk3 python-psutil`
