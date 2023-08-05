# @version ^0.3.0

"""
@title A contract for representing books onchain  
@license MIT
@author Obiajulu Mbanefo
@notice An contract aimed at implementating of a physical book on chain
"""

# Author of the book, represented by an address
Author: public(address)

# Title of the book
Title: public(String[256])

# Book license for IP rights purposes
License: public(String[256])

# Number of chapters in the book
Chapters: public(uint256)

# Chapter struct
struct Chapter:
    ispresent: bool
    name: String[256]
    chapterid: uint256
    content: String[1000000]

# Hashmap of uint256 and chapter struct that represents a book
Book: public(HashMap[uint256, Chapter])

# Sum of all ether sent to this contract
AllTimeValue: public(uint256)

# event fired upon chapter addition
event AddedChapter:
    Author: indexed(address)
    Chapter_id: indexed(uint256)
    Name: String[256]

# event fired upon chapter removal
event RemovedChapter:
    Author: indexed(address)
    Chapter_id: indexed(uint256)
    Name: String[256]

# event fired upon deposit
event Deposit:
    sender: indexed(address)
    value: uint256

# event fired upon withdrawal
event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

@external
def __init__(_title: String[256], _license: String[256]):
    self.Author = msg.sender
    self.Title = _title
    self.License = _license

@external
def addchapter(_chapter: uint256, _name: String[256], _content: String[1000000]) -> bool:
    """
    @notice Add a new chapter to the book
    @dev Add a new chapter to the book, only the author can call this method
    @param _chapter The chapter number, will throw error if chapter already exists
    @param _name The name of the chapter
    @param _content Contents of the chapter
    @return True if creation is successful
    """
    assert msg.sender == self.Author, "You are not authorized :) to do this"
    assert self.Book[_chapter].ispresent == False, "Chapter already exists"
    newChapter: Chapter = Chapter({
        ispresent: True,
        name: _name,
        chapterid: _chapter,
        content: _content
    })
    self.Chapters += 1
    self.Book[_chapter] = newChapter
    log AddedChapter(msg.sender, _chapter, _name)
    return True

@external
def removechapter(_chapter: uint256) -> bool:
    assert msg.sender == self.Author,  "You are not authorized :) to do this"
    assert self.Book[_chapter].ispresent == True, "Chapter doesnt exist"
    old: Chapter = Chapter({
        ispresent: self.Book[_chapter].ispresent,
        name: self.Book[_chapter].name,
        chapterid: self.Book[_chapter].chapterid,
        content: self.Book[_chapter].content
        })
    self.Book[_chapter] = empty(Chapter)
    self.Chapters -= 1
    log RemovedChapter(msg.sender, _chapter, old.name)
    return True


@external
def transfer( _to: address, _value: uint256):
    """
    @notice transfer ether deposited to this contract
    @dev transfer ether deposited to this contract, only the author can call this method
    @param _amount The amount of ether to transfer
    @param _to Address to send ether to
    """
    assert msg.sender == self.Author
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

@external
@payable
def __default__():
    self.AllTimeValue += msg.value
    log Deposit(msg.sender, msg.value)
