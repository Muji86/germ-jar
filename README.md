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

## Playing together on a TV

Everyone can play at once, each with their own phone or tablet, while the TV shows all the jars.

1. On the TV, open the game with `?tv` on the end (for example https://germ-jar-tv.web.app/?tv). It
   shows a QR code and a five-letter room code. The TV doesn't use a microphone.
2. Each player scans the QR code, picks or makes their player and allows the microphone. Each phone
   listens to the noise near it, so one loud player only upsets their own germs.
3. The TV shows a dish for every player, with their name, germs and full jars. New germs, MEGA germs
   and full jars are announced on the TV with the player's name. Click the TV page once to let it
   play sounds.

The QR code shrinks into the corner once someone has joined, so more players can join any time. A
phone that's switched away from the game shows as Paused on the TV. Progress is still saved on each
phone, the same as playing alone. The TV keeps the same room code between visits, so phones can
come back with the same link.

### More than one TV

The same game can be on several TVs at once, for example in two rooms. On the extra TV open
`https://germ-jar-tv.web.app/?tv=CODE` with the room code; the link is on the first TV's join card
and on the grown-up controls page. Every TV shows every player's dish and the announcements.

The first TV is the main one and owns the room. If it's switched off, another TV in the room takes over
straight away and the game carries on, keeping the grown-up's settings and removed players. A TV that
comes back with its usual `?tv` link rejoins the same game as an extra screen. The admin password is
kept apart from the room, so it carries on working after a takeover.

### Grown-up controls

The settings are changed from a grown-up's phone or computer, never on the TV:

1. Open `https://germ-jar-tv.web.app/?admin=CODE` (the link is on the TV's join card), or scan the QR
   code and tap **Grown-up controls** on the join page.
2. The first time, choose an admin password there. After that, grown-ups type it to get in, and each
   phone or computer remembers it for that room.
3. From there: how quiet it needs to be (Whisper, Calm or Chatty), how fast germs grow, whether germs
   pop or just hide when it's too loud, **Pause everyone**, a list of players with **Remove** (and
   **Let back in**), and **Change the admin password**. After a change, other grown-ups are asked
   for the new one.

The noise level is applied on top of each phone's own measured quiet room, so phones with different
microphones stay fair. While a phone is in a room those settings are greyed out in its Settings, and
its player's own settings come back when it plays on its own. The TV remembers the grown-up's
choices and removed players between visits.

The password is checked by the database rules: its hash is stored where nobody can read it, it can
only be chosen when the room has none yet (or changed by someone who knows it), and only a phone that
has proved it knows it can change settings or remove players. If a child chooses it first, the main
TV can reset it: move the mouse and click **Reset admin password**.

The phones and TV talk through a Firebase Realtime Database (project `germ-jar-tv`). Each device signs
in anonymously. A room holds only each player's name and a summary of their jar, the grown-up's settings and who
was removed, and it's deleted when the TV page closes. Nothing from the microphone is ever sent. The rules are in
`database.rules.json`; deploy changes with `firebase deploy --only database`.

https://germ-jar-tv.web.app/ is served by Firebase Hosting; publish changes with
`firebase deploy --only hosting` (only `index.html` is uploaded). When the TV page isn't on https
(opened as a file or from localhost), the QR code points phones at that copy.

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

`index.html?tv&demo` shows the TV screen with three pretend players. To try a real room in one
browser, open `?tv` in one tab and `?join=CODE&demo&name=Sam` in others (with `&fresh` to start
from one germ, or `&loud` to watch germs pop); demo tabs each sign in as a separate player. To try several
TVs in one browser add `&separate` to each TV tab (`?tv&separate`, then `?tv=CODE&separate`) so each
signs in on its own, as separate TVs would. Background
tabs pause the game, so bring a phone tab to the front to see it change on the TV.
