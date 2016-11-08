#!/usr/bin/python

from collections import OrderedDict as OD
from copy import deepcopy
import ldap

from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_DOUBLE, BOX_BLANK, BOX_HEAVY, BOX_LIGHT

import argparse

parser = argparse.ArgumentParser(description="display ldap tree")

parser.add_argument("-H", metavar='url',default="ldaps://localhost" , type=str, help="ldap url e.g. ldaps://localhost")
parser.add_argument("-b", metavar='searchbase', required=True , type=str, help="the searchbase")

args = parser.parse_args()




try:
	#l = ldap.initialize("ldaps://localhost")
	l = ldap.initialize(args.H)
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
	l.simple_bind_s()
except ldap.LDAPError, e:
	print e

baseDN = args.b
searchScope = ldap.SCOPE_SUBTREE

#retrieveAttributes = ["dn", "cn"]
retrieveAttributes = ["dn"]
searchFilter = "(objectClass=*)"

try:
	ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
	result_set = []
	while 1:
		result_type, result_data = l.result(ldap_result_id, 0)
		if (result_data == []):
			break
		else:
			## here you don't have to append to a list
			## you could do whatever you want with the individual entry
			## The appending to list is just for illustration. 
			if result_type == ldap.RES_SEARCH_ENTRY:
				result_set.append(result_data)
except ldap.LDAPError, e:
	print "error"
	print e


main_dic={}

def get_list_match(listA, listB):
        out=1
        if len(listA) + 1  == len(listB):
        	for i in xrange(1, len(listA) +1):
                	if listA[-i] != listB[-i]:
                        	out=0
        	if out == 1:
                	return listB
        	else:
                	return None

def get_items(dn):
	out=[]
        for item in result_set:
                dn_=item[0][0]
                tmp=dn_.split(",")
		t=get_list_match(dn,tmp)
		if t: 
			out.append(t)
	return out


def fill_dic_b(dic, dn):
        t = get_items(dn)
	str_dn=','.join(dn)
	for i in t:
		dic[str_dn]={}
		fill_dic(dic[str_dn], i)

def fill_dic(dic, dn):
        str_dn=','.join(dn)
	dic[str_dn]={}

        t = get_items(dn)
        for i in t:
                fill_dic(dic[str_dn], i)

fill_dic(main_dic, baseDN.split(","))

box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_LIGHT, horiz_len=1))
print(box_tr(main_dic))

