"""Second simple post-gen hook for testing project folder and custom file creation."""

print('post generation hook 2')
f = open('python_post_2.txt', 'w')
f.close()
