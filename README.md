<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://ununiquestorage.sfo2.cdn.digitaloceanspaces.com/VHLFansTextmark.png" alt="Logo" height="80">
  </a>

  <h3 align="center">Welcome to VHLFans (Server!)</h3>

  <p align="center">
    The one-stop-shop for all your VHL autocomplete needs. Except it's the backend, so it's 1/2 of what you need to *never* do VHL again ;)
    <br />
    <a href="https://chromewebstore.google.com/detail/vhlfans/ipajmabijmknmjncjnbpgncpnfcnpecg">Install extension (easy!)</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## VHLFans *Server* info

This is the boring, overly complex, spaghetti coded part of VHLFans. Essentially, when you click that infamous "cheat with VHLFans" button, your browser sends the stupid textbook questions over to this code, which scourers and scrapes the internet for relevant Quizlets. Running it yourself will cost money, as described below, so if you want to tinker around with VHLFans, I'd highly suggest tinkering with the frontend extension and leaving OpenAI billing to me 😭

**Top *server* FAQs:**

### How is this different from the main VHLFans extension?
This is the actual brains of VHLFans. VHLFans extension is essentially just a button that's added to your VHL Central activity, and when you click it, *Unicorn* by Noa Kirel (yep - that's the song! Israel's 2023 Eurovision entry) plays and a request gets sent to our server.
___
### Can I run VHLFans server myself?
Yes! There's no reason you should, but you can absolutely. Check out the getting started section below for more information :)
___
### Why *shouldn't* I run VHLFans myself?
VHLFans uses powerful, expensive technology to autofill VHL Central activities. Quizlet data is scraped using proxies, which, due to a *incredibly, incredibly* generous arrangement with ScraperAPI, is free for me to do, but would cost upwards of $50/mo to self-host. Furthermore, VHLFans is powered by OpenAI. OpenAI API keys are *super cheap*, but why not let me front the super cheap? 
___
### ELI5 how the server works!
The server takes your questions and sends them to GPT (see agents.py for the code!) OpenAI then calls two custom functions - search Quizlet and/or fetch lesson vocabulary (both happens in SERPer.py.) Searching Quizlet does exact what you used to do with VHL activates - it searches for a Quizlet deck with reliable answers. When VHL has a stupid creative writing prompt, our friends at OpenAI call fetch_vocabulary so the response it creates is relevant to the lesson and gets you an A!  
___


### Built With

VHLFans is made possible by people *far* smarter than me, but the most important one is ScraperAPI. Quizlet blocks normal bots from going to their website (rightfully so,) so we take advanced measures to disguise oursevles as normal people. Well, we don't, I'm not bright enough to, but ScraperAPI does. And they're generous enough to waive the cost for VHLFans, including for advanced JavaScript rendering features that costs them money. I'm beyond indebted to their amazing team. Check them out for all your scraping needs!

* [![ScraperAPI][ScraperAPI]][ScraperAPI-url] - The GOATs 👑
* [![PyCharm][PyCharm]][Jetbrains-url]
* [![Python][Python]][Python-url]
* [![OpenAI][OpenAI]][OpenAI-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Self-hosting VHLFans is *incredibly* easy! It does require some coding knowledge, but feel free to message me on GitHub if you want help setting it up.

### Prerequisites

You'll need Python, which you can download at https://python.org.

### Installation

Here comes the major life choice: do you use our preview or main branch? I push buggy, bad, code to our preview branch (which, FYI, you're *not* supposed to do), but our main branch is tested and stable. I'd recommend cloning the main one.
1. Clone the repo
<br>**Preview (⚠️ at your own risk!):**
    ```sh
   git clone https://github.com/owenhk/VHLFans2/tree/preview
   ```
   **Stable**
    ```sh
   git clone https://github.com/owenhk/VHLFans2/tree/main
    ```
2. Install requirements - Don't worry, it's not that big!
    ```sh
   pip3 install -r requirements.txt
   ```
3. Set your environment variables.
   1. ``DATABASE_URL`` - Your Postgres database URL (I recommend using [Railway](https://railway.com)), you can deploy one in like 15 seconds and then just copy the `DATABASE_URL`.
   2. ``OPENAI_API_KEY`` - Your OpenAI API key, get one at https://platform.openai.com
   3. ``SCRAPER_API_KEY`` - Your ScraperAPI key, which you can get at https://scraperapi.com/ - This is the expensive one.
   4. ``SERP_API_KEY`` - Your SerperDEV API key, which you can get at https://serper.dev
4. Power up!
    ```sh
   path/to/VHLFANs/VHLFans2/.venv/bin/python -m uvicorn app:app --reload
    ```

<!-- ROADMAP -->
## Roadmap
- [ ] AI voice generation with ElevenLabs to do speaking homework for you!
- [ ] Better caching linked to lessons instead of decks to reduce times significantly

See the [open issues](https://github.com/owenhk/VHLFans2/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/owenhk/VHLFans2/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=owenhk/VHLFans2" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the VHLFans ALMOST UN-LICENSED. See `LICENSE.txt` for more information.<br>FYI - this means you can do **whatever** the hell you want with this (unless you work for Vistas Higher Learning and want to patch it.)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/owenhk/VHLFans2.svg?style=for-the-badge
[contributors-url]: https://github.com/owenhk/VHLFans2/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/owenhk/VHLFans2.svg?style=for-the-badge
[forks-url]: https://github.com/owenhk/VHLFans2/network/members
[stars-shield]: https://img.shields.io/github/stars/owenhk/VHLFans2.svg?style=for-the-badge
[stars-url]: https://github.com/owenhk/VHLFans2/stargazers
[issues-shield]: https://img.shields.io/github/issues/owenhk/VHLFans2.svg?style=for-the-badge
[issues-url]: https://github.com/owenhk/VHLFans2/issues
[license-shield]: https://img.shields.io/github/license/owenhk/VHLFans2.svg?style=for-the-badge
[license-url]: https://github.com/owenhk/VHLFans2/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-Shameless_plug_😉-black.svg?style=for-the-badge&logo=instagram&colorB=b54cf0
[linkedin-url]: https://instagram.com/owenhillsklaus
[product-screenshot]: images/screenshot.png
[ScraperAPI]: https://img.shields.io/badge/ScraperAPI-1c22db?style=for-the-badge&logo=gnometerminal&logoColor=white
[ScraperAPI-url]: https://scraperapi.com
[PyCharm]: https://img.shields.io/badge/PyCharm-5bc3e2?style=for-the-badge&logo=pycharm
[Jetbrains-url]: https://jetbrains.com/
[Python]: https://img.shields.io/badge/Python_3.12-294360?style=for-the-badge&logo=python&logoColor=fae172
[Python-url]: https://vuejs.org/
[OpenAI]: https://img.shields.io/badge/Powered_by_OpenAI-bac5dd?style=for-the-badge&logo=openai&logoColor=black
[OpenAI-url]: https://openai.com/