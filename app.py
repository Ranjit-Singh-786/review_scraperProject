from flask import Flask,render_template,request,jsonify
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen as ureq

app = Flask(__name__)
@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')   # pass the html as a str

@app.route('/review',methods = [ 'GET','POST'])
def review():

    
    if request.method == 'POST':
        try:
            base_url = "https://www.flipkart.com"
            searching_product = request.form['content'].replace(" ","")  # requesting to the input box content by the name
            flipkrt_search_url = "https://www.flipkart.com/search?q="+searching_product
            uclient = ureq(flipkrt_search_url)   # main page where we will scrape the record
            flipkart_page = uclient.read()
            uclient.close()
            soup = BeautifulSoup(flipkart_page,'html.parser')
            bigboxes = soup.findAll("div", {"class": "_1AtVbE col-12-12"})  # class for particular products
            del bigboxes[0:3]      # for delete starting 3 elements
            box = bigboxes[0]
            productLink = base_url+box.div.div.div.a['href']   # get the linc at a particular page
            prodRes = requests.get(productLink)         # reached on the specific website
            prodRes.encoding = 'utf-8'   # encoded the content before pass BeautifulSoup
            soup2 = BeautifulSoup(prodRes.text,'html.parser')   # pass the webpage through the beautifulsoup
            commentboxes = soup2.find_all('div', {'class': "_16PBlm"})
            fil_name = searching_product + ".csv"
            fw = open(fil_name,'w')
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text

                except:
                    name = 'No Name'
                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text
                except Exception as e:
                    print("Exception while creating dictionary: ",e)

                mydict = {"Product": searching_product, "Name": name, "Rating": rating, "CommentHead": commentHead,
                            "Comment": custComment}
                reviews.append(mydict)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
   

    else:
        return render_template('index.html')



if __name__== "__main__":
    app.run(debug=True, port=5001)