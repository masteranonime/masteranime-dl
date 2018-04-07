# masteranime-dl

## Disclaimer

This software is for educational purposes ONLY.
It does NOT come with a warranty, express or implied.
Do NOT use this software to break the law in your local jurisdiction.
Also, this work is released under GPLv3.
Please read the `LICENSE` file for licensing details.


## Installing

Currently, this only works on Linux with `chromium-browser` and `chromedriver`.
It should be able to work on other platforms with other drivers,
but that's left as an exercise for the reader.

```bash
git clone https://github.com/masteranonime/masteranime-dl
cd masteranime-dl
./install_prereqs.sh
```


#### Installation Notes:

* I'm assuming `git` and `python` are already installed on your system
* I'm assuming you would like to use `chromium-browser` with `chromedriver` as the driver
* I'm assuming you'd like to be able to run the script in a headless environment (without graphics).
If not, you do not need to install `Xvfb`.
See below on how to disable using `Xvfb`.
* If you have `google-chrome` installed, you may want comment out the `chromium-browser` install line and see if it works.
If not, you can change it back and rerun the install script without issue.


## How to use it?

Like this:

```bash
user@host $ ./run.py
Email: my_email_address@email_host.com
Password: 
getting links...
```

Enter your account `email` and `password` and you will be logged in.
You won't be able to see your password as you type.
That's normal.


#### Disable Xvfb

AKA: What if I want to watch what the browser's doing?

If you want to watch what the browser is doing,
or if you just don't want to use `Xvfb`,
you can easily disable it.

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


