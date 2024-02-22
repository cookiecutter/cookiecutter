"""Simple post-gen hook for testing project folder and custom file creation."""

print('post generation hook')
f = open('python_post.txt', 'w')
f.close()
