# masteranime-dl

## Disclaimer

This software is for educational purposes ONLY.
It does NOT come with a warranty, express or implied.
Do NOT use this software to break the law in your local jurisdiction.

Also, this work is released under GPLv3.
Please read the `LICENSE` file for licensing details.


## Installing

Currently, this script only works on Linux with `chromium-browser` and `chromedriver`.
It should be able to work on other platforms with other drivers,
but that's left as an exercise for the reader.

```bash
git clone https://github.com/masteranonime/masteranime-dl
cd masteranime-dl
./install_prereqs.sh
```


#### Installation Notes:

* I'm assuming `git` and `python` are already installed on your system.
* I'm assuming you would like to use `chromium-browser` with `chromedriver` as the driver.
* I'm assuming you'd like to be able to run the script in a headless environment (without graphics).
If not, you do **not** need to install `Xvfb` (remove that package from the `install_prereqs.sh` script).
See below on how to disable using `Xvfb` if you decide to not install its package.
* If you have `google-chrome` installed, you may want to delete the `chromium-browser` line in `install_prereqs.sh`.
Otherwise, you'll have two versions of chrome installed.


## How to use it?

Like this:

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
Once it's finished running, take a look at the output folder with `ls output`.


#### Binge Watch

If you want to binge watch the shows (with `vlc output/[show]` for example),
you'll need to run `./pad_filenames.sh` first.

The downloader script doesn't know how many episodes are in a given show,
so it doesn't 0-pad the filenames.
This means they'll play in the wrong order given standard ordering
(unless you run the `./pad_filenames.sh` script first).


#### What it's doing

1. Logs into your account.
1. Visits your account's `my-anime` page and downloads links to each new episode you haven't viewed yet.
1. Visits each new episode link and downloads the video to the `output/` folder.
1. Repeats until there's nothing left on the `my-anime` page.


#### Disable Xvfb (to watch what the browser is doing)

##### Easy way

This is more of a hacky workaround than anything.
This is **not** considered "disabling Xvfb".
In order to do that, you'll need to follow the instructions in the next section.

Locate the following line in `run.py`:

```python
os.environ["DISPLAY"] = ":1.0"
```

Copy that line and paste it immediately underneath with "1.0" changed to "0.0".
It should look like this:

```python
os.environ["DISPLAY"] = ":1.0"
os.environ["DISPLAY"] = ":0.0"
```

If you want to make it go back to not showing the browser,
delete or comment the line you added.


##### Complete way

This is the proper way to disable `Xvfb`.
The "easy way" still runs `Xvfb` but just configures the rest of the script not to use it.

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


## Feedback

If you encounter any problems at all, feel free to open up issues about them.
Be sure to include the text printout of the error.


## Advanced

#### XPath

If you read the source, you'll notice a bunch of XPaths stored within.
These represent elements on the page that I need to send events to throughout the script's operation.
This is a poor way to accomplish this, but there's seldom a better way to.
It's also easy to update.


#### Real World Problems

This script doesn't handle missing links very well.
It decidedly does NOT retry different mirrors / qualities.
It just fails and adds that specific episode to a blacklist.

If you encounter an error that is caused by **one** link alone,
please make an issue about it because I consider that a serious flaw.
Problems with a single show should not affect any other shows.

This is a good way to find broken links, because that's often the only reason for failure.
Of course, if you find broken links please inform the site administrators.


#### Quality

Before you read this section, one **huge** caveat:
There is no support for mirrors other than `mp4upload` at the moment.
If you desire different mirror support, please create an issue requesting it.

The cookies that get injected into the page are used to ensure mirror and quality selection.
The default mirror is `mp4upload` and default quality `480p`, subbed.
If you wish to change this, you will need to follow these steps:

1. Navigate to any video page.
1. Select the mirror and quality you desire.
1. Open up your browser's debug interface. (in chrome, it's `Ctl+Shift+i`)
1. Locate where your cookies are stored. (in chrome, it's under Application > Cookies > masteranime)
1. Locate the `pref_host` and `pref_mirror` cookies.
1. Copy down both of their values.
1. Set these values to the `pref_host` and `pref_mirror` cookies, respectively, in the `set_content_cookies` function of `run.py`

The cookie settings only represent the defaults, however.
If your chosen mirror / quality don't exist, the site will default to the first in the available list.

If you don't want to change the mirror (`pref_host`), then you don't have to.
You can change the quality independently.
The quality format seems to be `[subs]&3B[qual]` where subtitles are indicated with a `1`, and the quality is listed directly.
(if you're curious, the `&3B` is used to represent a semicolon).


