Games
=====
This directory will host games for the Math Orientation site.  In genral, we will try to keep
the clutter of the games development out of this directory and instead import them as `git-submodules`.
Documentation on using `git-submodules` can be found here: https://git-scm.com/book/en/v2/Git-Tools-Submodules

## Adding a Game
To add a game, you first want to create a directory for that project.  For simplicity, let's assume my game is
"Racket and Clang" (not that python paths cannot contain hyphens or spaces, so we'll replace our spaces with underscores).
First I create my directory
```
$ cd games
$ mkdir racket_and_clang
```
Then I have to add a `views.py` to serve my game, so create one in the directory.  After doing that, you'll need to add an
entry for your game to the Games listing, so go to the admin page and create a new Game entry.  By default, the `index.html`
page in the root directory of the game directory is always served.

## Adding the Git Submodule
Since you'll want to work on the game in another project, you'll want to have those files available to the site.  To do so, you
should add a Git Submoudule for your project.  Simply add the project to the `.gitmodules` file as so:
```
[submodule "Racket-and-Clang"]
  path = games/racket_and_clang
  url = https://github.com/mathorient/racket-and-clang
```

## Models
### Game
To have the games appear on the games index page, you need to add a model for the Game to the listing.  The Game models allows
you to define the name of the game and a slug (for the url).
