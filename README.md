# Germ Jar

**Play it: https://ben-pearson.github.io/germ-jar/**

A calm-noise game for home, based on the idea behind [Shy Safari](https://www.shysafari.com/).
A microphone listens to how loud the room is. While it stays under the goal, the germs in the
jar split and multiply. Too loud for a few seconds and they go pale and hide, and one pops
(splat, then a little ghost floats away). Another pops every 4 seconds while it stays loud, but
the last germ never pops. Settings can switch this to "Germs just hide", where growth only
pauses. Fill the jar (64 germs) for a celebration and a jar on the shelf.

Each split has a chance of making a different kind of germ. Rarities, commonest first: common,
uncommon, rare, epic, legendary, mythic. Seasonal germs only appear in their months, three times
as often as their rarity suggests:

- Easter (March and April): Easter Egg, Bunny, Chick, Golden Egg
- Halloween (October): Pumpkin, Mummy, Witchy, Frankengerm, Vampire
- Bonfire Night (November): Sparkler, Toffee Apple, Rocket, Firework
- Christmas (December): Snowman, Elf, Reindeer, Gingerbread, Santa
- Birthday (the player's birthday month, set in Settings): Present, Birthday Germ

The Collection screen shows what's been found, grouped by season. New germs go in the `TYPES`
list in `index.html`; a seasonal one needs `season` and `months`.

Three germs of the same kind that stay safe for a long time (40 splits' worth of calm, set by
`MEGA_AFTER`) drift together and join into one MEGA germ: bigger, with a turning gold ring. It
fills three places in the jar, never pops and never splits. About one per jar.

## Players

Each player has their own germs, jars, collection and settings, so a "Test" player on Test
speed never touches anyone else's progress. The start screen asks who's playing; Settings has
Switch player, Rename, Reset this player and Delete this player. A save from before players
existed becomes "Player 1".

## Password

Settings can be locked with a password (Settings, Password). Once set, opening Settings and making
a new player need it, and any player can be marked "Ask for the password to play as this player"
(handy for a Test player on Test speed). New players always start at Normal speed. The password
is stored as a hash in the browser and is shared by all players. It keeps a 6 year old out, not a
determined grown-up.

Forgotten it? In Chrome on that computer press F12, open Console, run
`localStorage.removeItem('germjar.lock')` and reload. Players and progress are untouched.

## Running it

Open the link above (or `index.html`) in Chrome or Edge, pick or make a player and allow the
microphone. It works well full screen on a TV with a USB microphone or webcam mic. On the first run it measures the room for 5 seconds to set the goal.

- **F** or the Full screen button: full screen on the TV
- **Space**: pause
- **S**: settings (player; goal: Whisper, Calm or Chatty; speed; what happens when it's too
  loud; birthday month; which microphone; sounds)
- **C**: collection
- **J** or the Jars button (or click the little jars in the corner): the jar shelf; click a
  full jar to look inside it

Progress is saved in the browser (localStorage), so it carries on between days. Use the same
browser and address each time; a copy opened from another address has its own separate players.
Nothing is recorded or sent anywhere: the microphone is only used to measure how loud the room is.

When opened as a file, Chrome may ask for the microphone every time. To make it remember,
serve the folder locally and open `http://localhost:8000` instead:

```
python -m http.server 8000
```

## Hosting it yourself

The easiest way is the GitHub Pages copy above: it's https, so the microphone just works. To run
it on your own home server instead, note that Chrome only allows the microphone on https (or
localhost) pages. `serve.py` serves `public/index.html` over https on port 5008 and redirects plain
http to it:

1. Make a certificate for the server's address. A small certificate authority of your own works
   well: create it with openssl (ideally name constrained to just that address), sign a server
   certificate with it, and put `server.crt` and `server.key` in `~/.germ-jar-tls/`.
2. Copy `index.html` into `public/` next to `serve.py` and run `python3 serve.py` (a systemd
   service keeps it running).
3. On each computer that plays it, install your authority's certificate as a trusted root once.

## Testing

`index.html?demo` runs with a fake microphone and fast growth, saving nothing.
Extra options: `&sim=60` runs 60 seconds of game time straight away, `&loud` makes it too
loud, `&open=collection`, `settings`, `shelf` or `jar` opens a panel, `&all` puts every germ type in
the dish and collection, `&megas` marks MEGA germs as found, `&fresh` starts from one germ,
`&megaafter=12` changes the MEGA threshold, and `&month=10` pretends it is October.
