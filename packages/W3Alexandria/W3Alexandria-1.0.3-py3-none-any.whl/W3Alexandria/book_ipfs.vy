# @version ^0.3.0

"""
@title A contract for representing books onchain  
@license MIT
@author Obiajulu Mbanefo
@notice An contract aimed at implementating of a physical book on chain via ipfs
"""

# Author of the book, represented by an address
Author: public(address)

# Title of the book
Title: public(String[256])

# Book license for IP rights purposes
License: public(String[256])

# book format as uploaded to ipfs, used to build the book from the hash
BookFormat: public(String[128])

# hash of book after it is hosted on ipfs 
IpfsHash: public(String[256])

# Sum of all ether sent to this contract
AllTimeValue: public(uint256)

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
def __init__(_title: String[256], _license: String[256], _ipfshash: String[256], _bookformat: String[128]):
    self.Author = msg.sender
    self.Title = _title
    self.License = _license
    self.IpfsHash = _ipfshash
    self.BookFormat = _bookformat

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
