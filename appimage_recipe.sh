#!/usr/bin/env bash
# Pyslvs AppImage Recipe

########################################################################
# Create the AppDir
########################################################################

APP=pyslvs
LOWERAPP=${APP,,}

mkdir -p ENV/$APP.AppDir/
cd ENV/$APP.AppDir/

########################################################################
# Create a virtualenv inside the AppDir
########################################################################

mkdir -p usr
virtualenv --always-copy --python=python3 ./usr

source usr/bin/activate

# Source some helper functions
wget -q https://raw.githubusercontent.com/AppImage/AppImages/master/functions.sh -O ./functions.sh
. ./functions.sh

#Show python and pip versions
which python
which pip

# Install python dependencies into the virtualenv
pip install -r ../../requirements.txt

########################################################################
# "Install" app in the AppDir
########################################################################

cp ../../launch_pyslvs.py usr/bin/$LOWERAPP
sed -i "1i\#!/usr/bin/env python3" usr/bin/$LOWERAPP
chmod a+x usr/bin/$LOWERAPP

cp ../../icons_rc.py usr/bin
cp ../../preview_rc.py usr/bin
cp -r ../../core usr/bin

rm -fr usr/bin/core/libs/pyslvs/build
rm -fr usr/bin/core/libs/pyslvs/src
rm -fr usr/bin/core/libs/pyslvs/Adesign
rm -fr usr/bin/core/libs/python_solvespace/obj
rm -fr usr/bin/core/libs/python_solvespace/include
rm -fr usr/bin/core/libs/python_solvespace/src
find . -type f -name '*.ui' -delete

########################################################################
# Finalize the AppDir
########################################################################

get_apprun

cd ../..
VERSION=$(python3 -c "from core.info.info import __version__; print(\"{}.{:02}.{}\".format(*__version__))")
cd ENV/$APP.AppDir/

cat > $LOWERAPP.desktop <<EOF
[Desktop Entry]
Name=$APP
Exec=$LOWERAPP
Type=Application
Icon=$LOWERAPP.png
StartupNotify=true
Comment=Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
EOF

# Make the AppImage ask to "install" itself into the menu
get_desktopintegration $LOWERAPP
cp ../../icons/main_big.png $LOWERAPP.png

########################################################################
# Bundle dependencies
########################################################################

copy_deps ; copy_deps ; copy_deps
delete_blacklisted
move_lib

########################################################################
# Package the AppDir as an AppImage
########################################################################

cd ..
generate_appimage
