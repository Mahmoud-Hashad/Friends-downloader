# Friends-downloader
A simple web scraper to download all episodes of the friends series

The script scrap a server that contains all episodes of friends 

Total of 235 episode
Server Url: [http://s8.bitdl.ir/Series/friends/]("http://s8.bitdl.ir/Series/friends/")

All the downloaded episodes will be saved in a directory called `Friends` at the same directory 

```
Friends/
+-- S01/
|   +-- Friends.S01E01.720p.Bia2HD.mkv
|   +-- Friends.S01E02.720p.Bia2HD.mkv
|   +-- ...
|   +-- Friends.S01E24.720p.Bia2HD.mkv
+-- S03/
+-- ...
+-- S09/
+-- S10/
|   +-- Friends.S10E01.720p.Bluray.Bia2HD.mkv
|   +-- ..
|   +-- Friends.S10E19-E20.720p.Bluray.Bia2HD.avi
```




You can stop the script at any point and the next time it runs will not overwrite the downloaded vides

The total download size is 34G
```bash
mahmoud@ubuntu:~/Friends-downloader$ du -h Friends/
2.9G    Friends/S10
3.5G    Friends/S03
3.4G    Friends/S09
3.8G    Friends/S02
3.3G    Friends/S08
3.3G    Friends/S04
3.5G    Friends/S06
3.3G    Friends/S01
3.3G    Friends/S05
3.3G    Friends/S07
34G     Friends/

```

## Usage
- Create a virtual environment
```
virtualenv venv
```
- install dependencies
```
pip3 install -r requirements.txt 
```
- Some vairables to change
  - `BASE_FOLDER`: The saving directory
  - `THREADS` : Number of concurrent threads that run simultaneously to speed up the download the number of threads will depend on your system resources
- Run the script
```
python3 main.py
```
