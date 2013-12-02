import os,sys,subprocess
from urlparse import urlparse
""" Find all files in the Download Folder and sort them into folders, according to the source of download.
Inspects the kMDItemWhereFroms download field, that Chrome (and Safari!? ) sets on downlaoded files.
The information can be obtained with the mdls utility on the mac.
"""

import platform
if platform.system() != 'Darwin':
	print "sorry, only mac supported"
	exit(2)

down_folder = "/Users/martinfaust/Downloads/"

def parse_output(inps):
	"""parses the mdsl output and returns the domain from where a certain file was downloaded"""
	# 	kMDItemWhereFroms = (
	#     "http://surfnet.dl.sourceforge.net/project/grandperspectiv/grandperspective/1.5.1/GrandPerspective-1_5_1.dmg",
	#     "http://sourceforge.net/projects/grandperspectiv/files/grandperspective/1.5.1/GrandPerspective-1_5_1.dmg/download"
	# )
	inps = inps[len("kMDItemWhereFroms = ("):-3]
	inps = inps.split("\n")
	reversedinp = inps[::-1]
	# find first one that starts with http
	down_from = ''
	for x in reversedinp:
		if "http" in x or "ftp" in x:
			down_from = x

	down_from = down_from.strip()
	# remote litter
	if down_from:
		if down_from[0] == '"': down_from = down_from[1:]
		if down_from[-1] == ',': down_from = down_from[:-1]
		if down_from[-1] == '"': down_from = down_from[:-1]
	# parse the domain value
	o = urlparse(down_from)
	return o.netloc




for f in os.listdir(down_folder):
	# print "================="
	# print f
	try:
		s= subprocess.check_output(["mdls","-name","kMDItemWhereFroms","%(down_folder)s%(filename)s"%({"down_folder":down_folder, "filename":f})])
	except subprocess.CalledProcessError, e:
		print "failed to get info on file:",f , " Error:", e
	loc= parse_output(s)
	#reverse the location
	rev_loc = ".".join(loc.split(".")[::-1])
	if rev_loc:
		try:
			target_dir = "%s%s"%(down_folder,rev_loc)
			os.mkdir(target_dir)
		except OSError,e :
			print e

		print "mv ", f, "%s/"%rev_loc
		try:
			target_file  = "%s/%s" %(target_dir,f)
			try:
				os.stat(target_file)
			except OSError,e :
				pass
			else:
				assert("File is already there, cowardly exiting. (Double download?)")
				# FIXME: Rename file, append suffix.
				exit(1)
			os.rename("%s%s"%(down_folder,f), target_file)
		except:
			print "move fail."



