from textnode import *

def main():
    testObj = TextNode("Testing", "text")
    testObj2 = TextNode("URL test", "link", "https://www.youtube.com")
    testObj3 = TextNode("Testing", "text")
    print(testObj)
    print(testObj2)

main()