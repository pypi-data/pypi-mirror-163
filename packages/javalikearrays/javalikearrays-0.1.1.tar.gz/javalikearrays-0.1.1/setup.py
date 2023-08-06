from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='javalikearrays',
  version='0.1.1',
  description='Java array functionality in Python :: Development Build',
  long_description=open('README.txt').read(),
  url='https://github.com/alpheay/JavaLike.git',  
  author='Sagnik Nandi',
  author_email='nik.nandi.1@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='arrays', 
  packages=find_packages(),
  install_requires=[''] 
)