import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import http.requests.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class BookOfSands8 extends PApplet {

// Murtaza Tunio 2018
// Book of Sands
// Re-Write: 7 with flipping and buffer


PFont f;
int buffer_len = 5;
ArrayList<String[]> buffer = new ArrayList<String[]>(buffer_len); 
int dex = 0;
int state = 0;
String[] blank = {"",""};
int maxQuery = 58000;


public void setup(){
  frameRate(25);
  background(242,222,189);
  
  fill(0);
  f = createFont("LucidaSans", 16);
  
  PImage titlebaricon = loadImage("icon.png");
  surface.setIcon(titlebaricon);
  surface.setTitle("The Book of Sands");
  String offers = urlRequest("https://www.gutenberg.org/ebooks/");
  int indexoffers = offers.indexOf("offers");
  try { maxQuery = PApplet.parseInt(trim(offers.substring(7+indexoffers,14+indexoffers).replace(",","")));}catch(Exception e){};
}

public void draw(){
  switch(state){
    case 0:
      background(242,222,189);
      textFont(f);
      text("loading...",30,30);
      if (frameCount % 10 == 0){
        thread("addToBuffer");
      }
      if (millis()>20000){
        state++;
      }
      break;
    case 1:  
      background(242,222,189); 
      textFont(f);   
      text("Click to change the page; study the page well. You will never see it again...", 18, 30);
      state++;
      break;
    case 2:
      if (frameCount % 10 == 0 && buffer.size() - dex < 50){
        thread("addToBuffer");
      }
      if (frameCount % 250 == 0){
        println("garbage_collection...");
        for(int i = 0; i+1 < dex; i++){
          buffer.set(i,blank);
        }
      }
  }
}

public String urlRequest(String URL){
  println("requesting url...");
  GetRequest get = new GetRequest(URL);
  get.addHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8");
  get.addHeader("Accept-Encoding", "unicode");
  get.addHeader("Accept-Language", "en-US,en;1=0.5");
  get.addHeader("Cookie", "bonus=id7460; session_id=7c7d019c522c8362f49d8b61302af1815280a0c5");
  get.addHeader("DNT", "1");
  get.addHeader("HOST", "www.gutenberg.org");
  get.addHeader("Upgrade-Insecure-Requests", "1");
  get.addHeader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0");
  get.send();
  return get.getContent();
}


public String getbook(boolean triedA, int X) {
  println("getting book...");
  String base_url_a = "https://www.gutenberg.org/files/X/X-0.txt";
  String base_url_b = "https://www.gutenberg.org/cache/epub/X/pgX.txt";
  String book;
  if(triedA) {
    book = urlRequest(base_url_b.replace("X", str(X)));
  } else {
    X = PApplet.parseInt(random(1,maxQuery));
    book = urlRequest(base_url_a.replace("X", str(X)));
    if (book.contains("404 Not Found")) {
      book = getbook(true, X);
      if (book.contains("404 Not Found")) {
        book = getbook(false, 0);
      } 
    }   
  }   
  return book;
}


public String getMeta(String full){
  println("getting metadata...");
  String[] lines = full.split("\n");
  String meta = "";
  for (int i = 0; i < lines.length; i++){
    String here = lines[i];

    if (here.contains("Title:")) {meta = meta + here + " " + trim(lines[i+1]) + "\n";}
    if (here.contains("Author:")) {meta = meta + here + ", ";}
    if (here.contains("Release Date:")) {
      try { here = trim(here.split(",")[1]);} 
      catch(Exception e) { here = trim(here);}
      if (here.contains("EBook") | here.contains("eBook") | here.contains("Etext")) { here = here.split(" ")[0];}
      meta = meta + here + "\n";}
    if (here.contains("Language:")) {meta = meta + trim(here) + "\n";}
  }
  if(trim(meta)==""){
    return "NO META DATA \n\n no meta data \n\n no meta data";
  }
  return meta;
}


public String choosePart(String full){
  println("choosing page...");
  int show_lines = 30;
  full = full.replace("\n\n\n","\n\n")
             .replace("\n \n\n","\n\n")
             .replace("\n\n \n","\n\n")
             .replace("\n \n","\n")
             .replace("\n\n","\n");
  String[] lines = full.split("\n");
  int num_lines = lines.length;
  int mark0 = PApplet.parseInt(random(30,num_lines-30));
  while(lines[mark0].trim().isEmpty()){
    mark0++;
  }
  if (show_lines + mark0 > num_lines){
    show_lines = num_lines - mark0;
  }
  return join(subset(lines,mark0,show_lines),"\n");
}


public String[] getpage(){
  println("getting view...");
  String[] out = new String[2];
  String fulltext = getbook(false,0);
  String[] fulltext_metasplit = fulltext.split("PROJECT GUTENBERG");
  String meta = getMeta(fulltext_metasplit[0]);
  fulltext = fulltext_metasplit[1];
  String part = choosePart(fulltext).replace("_","");
  out[0] = meta + "\n \n \n";
  out[1] = part;
  return out;
}

public void fittedText(String text, PFont font, float posX, float posY, float fitX, float fitY) {
  textFont(font);
  float suggest_size = max(10, min(min(font.getSize()*fitX/textWidth(text), fitY),20));
  textSize(suggest_size);
  text(text, posX, posY, width+1, height-30-60);
}

public void showPage(String[] page){
    println("displaying page...");
    background(242,222,189);
    String meta = page[0];
    String pagein = page[1];
    textFont(f);
    textLeading(16);
    text(meta,30,28);
    fittedText(pagein, f, 30, 30 + 60, width - 60, height - 60);
}


public void mousePressed(){
  println("index: " + dex + ",", "buffered: " + buffer.size());
  if(state==2){
    if(dex+1==buffer.size() | state == 0){
      showPage(buffer.get(dex));
    } else {
      showPage(buffer.get(dex));
      dex++;
    }
  }
}

public void addToBuffer(){
  println("adding to buffer...");
  buffer.add(getpage());
}
  public void settings() {  size(680,900);  smooth(); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "--present", "--window-color=#666666", "--stop-color=#F2DEBD", "BookOfSands8" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
