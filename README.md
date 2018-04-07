# masteranime-dl


## Installing

Currently, this script only works on Linux with `chromium-browser` and `chromedriver`.
It should be able to work on other platforms with other browsers and their drivers,
but that's left as an exercise for the reader.

```bash
git clone https://github.com/masteranonime/masteranime-dl
cd masteranime-dl
./install_prereqs.sh
```

See advanced section below for installation notes and considerations.


## Usage

#### Download everything you follow

```bash
user@host $ ./run.py

Email: my_email_address@email_host.com
Password: 
getting links...
-- snip --
```

Enter your account `email` and `password` and you will be logged in.
You won't be able to see your password as you type.
That's normal.

Keep in mind that the script usually takes a *very* long time to complete.
You'll want to leave it running overnight (longer, if you have a large number of shows queued up).
Once it's finished running, you can see what was downloaded by inspecting the `output/` folder.


#### Binge watch everything

```bash
user@host $ ./pad_filenames.sh
user@host $ vlc output
```


#### Binge watch single show

```bash
user@host $ ./pad_filenames.sh
user@host $ vlc output/show-title
```


#### Watch single episode

```bash
user@host $ ./pad_filenames.sh
user@host $ vlc output/show-title/01.mp4
```

## What it's doing

1. Logs into your account.
1. Visits your account's `my-anime` page and downloads links to each new episode you haven't viewed yet.
1. Visits each new episode link and downloads the video to the `output/` folder.
1. Repeats until there's nothing left on the `my-anime` page.


## Feedback

If you encounter any problem at all, feel free to open up issue about it.
Be sure to include the text printout of the error.


## Advanced

#### Installation Notes:

* I'm assuming `git` and `python` are already installed on your system.
* I'm assuming you would like to use `chromium-browser` with `chromedriver` as the driver.


##### Avoid package bloat

I dislike installing packages that aren't 100% necessary.
If you're the same way, please consider the following:

1. If you already have `google-chrome` installed,
you may want to open up `install_prereqs.sh` and delete the `chromium-browser` install line.
Otherwise, you'll have two copies of a similar browser on your system.
You may want to keep both to maintain profile separation,
but selenium-controlled browser sessions are sandboxed from your normal profile anyway.
They don't even come with your normally-loaded extensions.

1. Consult the following flow chart to decide how to handle `Xvfb`:

```
Desire ability to run the script in a
headless (no graphics) environment? ----- yes -----> leave Xvfb alone
           |
           no
           |
Desire browser window to be
invisible while script is running? ------ yes -----> leave Xvfb alone
           |
           no
           |
You don't need Xvfb. Get rid of it.
```

If you've decided to get rid of `Xvfb`, you'll need to do two things.

1. Open up the `install_prereqs.sh` file and remove the `Xvfb` install line.
1. Follow the `Disable Xvfb` section below


#### Disable Xvfb (to watch what the browser is doing)

Open up `run.py` and locate the following (it's right at the top):

```python
# Don't want to use Xvfb? Uncomment the following line:
# """
```

Turn that into:

```python
# Don't want to use Xvfb? Uncomment the following line:
"""
```

and you're good to go!


#### XPath

If you read the source, you'll notice a bunch of XPaths stored within.
These represent elements that I need to send events to at various points in the script's execution.
This is a poor way to accomplish element location because it's so fragile,
but it's very easy to update.


#### Real World Problems

This script doesn't like missing or broken links.
It decidedly does **not** retry different mirrors / qualities.
It just fails and adds that specific episode to an internal blacklist.
This blacklist gets cleared between each run.
Additionally, if you check that episode off in your account,
it won't be there for the next run (and the problems might go away as well).

If you encounter an error that fails due to some sort of URL issue
(you'll see the error printed clearly),
please report it to the site's administrators.
You can do that through [this form here](https://docs.google.com/forms/d/e/1FAIpQLSfGfBZY_y4bvXVxHmb7pTpk2DL_DoHaEgiOMXXHMIMqIiiPxA/viewform?c=0&w=1&usp=send_form).


#### Quality

Before you read this section, one **huge** caveat:
There is no support for mirrors other than `mp4upload` at the moment.
If you desire different mirror support, please create an issue requesting it.

The cookies that get injected into the page are used to ensure mirror and quality selection.
These cookie settings only represent the defaults, however.
If your chosen mirror / quality don't exist, the site will default to the first option in the available list.

The default mirror is `mp4upload` and default quality `480p`, subbed.
If you wish to change this script behavior, you will need to follow these steps:

1. Navigate to any video page.
1. Select the mirror and quality you desire.
1. Open up your browser's debug interface. (in chrome, it's `Ctl+Shift+i`)
1. Locate where your cookies are stored. (in chrome, it's under Application > Cookies > masteranime)
1. Locate the `pref_host` and `pref_mirror` cookies.
1. Copy down both of their values.
1. Set these values to the `pref_host` and `pref_mirror` cookies, respectively, in the `set_content_cookies` function of `run.py`

If you don't want to change the mirror (`pref_host`), then you can leave it as is.
You can change the quality independently.
The quality format seems to be `[subs]&3B[qual]` where subtitles are indicated with a `1`, and the quality is listed directly.
(if you're curious, the `&3B` is used to represent a semicolon).


