# @version ^0.3.0

"""
@title Alexandria
@license MIT
@author Obiajulu Mbanefo
@notice A contract that aids indexing literary information on the metaverse.
"""
# Library name
LibraryName: public(String[256])

# The librarian
Librarian: public(address)

# Number of books in the library
BookCount: public(uint256)

# Sum of all ether sent to this contract
AllTimeValue: public(uint256)

# A random string  
Quote: public(String[1024])

# Book struct
struct Book:
    ispresent: bool
    bookaddr: address
    author: address
    title: String[256]

# Hashmap of uint256 and Book struct to represent a physical library
Library: public(HashMap[uint256, Book])

interface GetBook:
    def Title() -> String[256]: view
    def Author() -> address: view

# event fired when a book is added
event AddBook:
    librarian: indexed(address)
    bookaddr: indexed(address)
    author: indexed(address)
    title: String[256]

event RemoveBook:
    librarian: indexed(address)
    bookaddr: indexed(address)
    author: indexed(address)
    title: String[256]

# event fired when upon deposit
event Deposit: 
    sender: indexed(address)
    value: uint256

# event fired upon withdrawal
event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

@external
def __init__(_library_name: String[256]):
    self.LibraryName = _library_name
    self.Librarian = msg.sender
    self.Quote = "'How dare you and the rest of your barbarians set fire to my library? \n Play conqueror all you want, Mighty Caesar! Rape, murder, pillage thousands, even millions of human beings! \n But neither you nor any other barbarian has the right to destroy one human thought!'\n \n" #  - Sidney Buchman

@payable
@external
def __default__():
    self.AllTimeValue += msg.value
    log Deposit(msg.sender, msg.value)

@internal
@view
def gettitle(_addr: address) -> String[256]:
    return GetBook(_addr).Title()

@internal
@view
def getauthor(_addr: address) -> address:
    return GetBook(_addr).Author()

@external
def addbook(_id: uint256, _bookaddr: address) -> bool: 
    """
    @notice Add a new book to the library
    @dev Add a new book to the library, only the librarian can call this method
    @param _id The book number in the library
    @param _bookaddr Contract address of the book
    @return True if creation is successful
    """
    assert msg.sender == self.Librarian, "only the librarian can call this method"
    assert self.Library[_id].ispresent == False, "id is already taken"
    _author: address = self.getauthor(_bookaddr)
    _title: String[256] = self.gettitle(_bookaddr)
    new: Book = Book({
        ispresent: True,
        bookaddr: _bookaddr,
        author: _author,
        title: _title
    })
    self.Library[_id] = new
    self.BookCount += 1
    log AddBook(msg.sender, _bookaddr, _author, _title)
    return True

@external
def removebook(_id: uint256) -> bool: 
    """
    @notice Remove a book from the library
    @dev Remove a book from the library, only the librarian can call this method
    @param _id The book number in the library
    @return True if removal is successful
    """
    assert msg.sender == self.Librarian, "only the librarian can call this method"
    assert self.Library[_id].ispresent == True, "there is nothing here"
    old: Book = Book({
        ispresent: self.Library[_id].ispresent,
        bookaddr: self.Library[_id].bookaddr,
        author: self.Library[_id].author,
        title: self.Library[_id].title
        })
    self.Library[_id] = empty(Book)
    self.BookCount -= 1
    log RemoveBook(msg.sender, old.bookaddr, old.author, old.title)
    return True

@external
def transferposition(_new_librarian: address) -> bool: 
    """
    @notice Change Librarian
    @dev Change Librarian, can only be called by the librarian
    @param _new_librarian Change librarian
    """
    assert msg.sender == self.Librarian, "only the librarian can call this method"
    self.Librarian = _new_librarian
    return True

@external
def transfer( _to: address, _value: uint256):
    """
    @notice transfer ether deposited to this contract
    @dev transfer ether deposited to this contract, only the librarian can call this method
    @param _amount The amount of ether to transfer
    @param _to Address to send ether to
    """
    assert msg.sender == self.Librarian, "only the librarian can call this method"
    send(_to, _value)
    log Transfer(msg.sender, _to, _value)

@external
@view
def balanceof() -> uint256:
    """
    @notice Return contract eth balance
    @dev Return contract eth balance
    @return uint256
    """
    return self.balance
