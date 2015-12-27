'''
This program searches the NYPL catalogue.
The input is a spreadsheet containing book titles and authors.
It is set currently to only return ebooks, but this could be adjusted in the code.
The output is currently a command line list of results.
'''

import xlrd, xlwt
from selenium import webdriver
from selenium.webdriver.support.ui import Select


## Substantiate webdriver
driver = webdriver.PhantomJS()


## Read in Excel info
print "Logging: Opening Excel file" # Open Excel file
book = xlrd.open_workbook('source_sheet.xls') # Select the first sheet in workbook
data = book.sheet_by_index(0) # Select the first column and remove header to make list of titles
print "Reading in list of book titles"
book_titles = data.col_values(colx=0)[1:]
print book_titles

## Do search for book titles
results_yes = [] # List to save responses - will be final output
results_no = []
for book in book_titles:
    print "Logging: In Book title search loop"
    print "Book = ", book

    ## Go to advanced search PAGE
    driver.get("http://ebooks.nypl.org/AdvancedSearch.htm")
    #print driver.title, driver.current_url

    ## Fill in the book title -- unlike NYPL web UI itself this is exact match search
    #print "Logging: Filling book title"
    book_title = driver.find_element_by_name('Title')
    book_title.send_keys(book)

    ## Select all Ebook formats only
    #print "Logging: selecting ebooks only"
    select = Select(driver.find_element_by_id('formatSelect'))
    select.select_by_visible_text('All eBooks')

    #print "Logging: Submitting book title"
    driver.find_element_by_xpath('//*[@id="advSearchSubmit"]/div/input').click()

    ## We're now on search results page
    #print driver.title, driver.current_url

    ## Count number of titles/results occurring on page, today, for Hobbit, there should be 15
    num_titles = driver.find_elements_by_class_name('tc-title')

    if not num_titles:
        result = "%s: No ebook results found" % book
        results_no.append(result)
        #print result
    else:
        num_results = 0
        avail_copies = 0
        for title in num_titles:
            #print title.text
            num_results += 1
            ## Find out if it's available
            ## Get the id of the item
            book_url = title.get_attribute('href') # returns format http://ebooks.nypl.org/A02A5CF2-504D-45F9-B4B7-36502E3FD14D/10/50/en/ContentDetails.htm?id=2E99EA1C-9E85-49F4-AFEF-4EDA4C20BBBF
            book_id = book_url.split("=")[1]

            ## Now find the div w class data-info containing the book_id
            crid = 'data-thiscrid='+'"'+book_id+'"'
            info_span_contents = driver.find_element_by_css_selector("a["+crid+"]")
            avail_copies = int(info_span_contents.get_attribute('data-availcopies'))

        result = "%s: %d ebook results found w/ %d avail copies" % (book, num_results, avail_copies)
        results_yes.append(result)
        #print result

print "BOOKS NOT FOUND"
print results_no

print "BOOKS FOUND"
print results_yes





