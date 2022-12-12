#! /bin/bash
echo "Packaging YouTube for release..."
mkdir release
mkdir release/out
cp -r YouTube modules README.md release
zip -r release/out/plugin.video.youtube.zip modules YouTube README.md
echo "Finished!"
