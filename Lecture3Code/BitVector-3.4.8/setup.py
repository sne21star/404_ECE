#!/usr/bin/env python

### setup.py

#from distutils.core import setup

from setuptools import setup, find_packages

setup(name='BitVector',
      version='3.4.8',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/dist/BitVector-3.4.8.html',
      download_url='https://engineering.purdue.edu/kak/dist/BitVector-3.4.8.tar.gz',
      description='A memory-efficient packed representation for bit arrays in pure Python',
      long_description='''



Consult the module API page at

    https://engineering.purdue.edu/kak/dist/BitVector-3.4.8.html

for all information related to this module, including                                       
information regarding the latest changes to the code. The                                   
page at the URL shown above lists all of the module                                         
functionality you can invoke in your own code.

With regard to the basic purpose of the module, it defines
the BitVector class as a memory-efficient packed
representation for bit arrays. The class comes with a large
number of methods for using the representation in diverse
applications such as computer security, computer vision,
etc.

**Version 3.4.8** fixes a bug in the slice assignment logic in the                                implementation of __setitem__().

**Version 3.4.7** fixes a Python 3 specific bug in the
write_to_file() method of the module.  While I was at it, I
have also changed the name of the method
write_bits_to_fileobject() to write_bits_to_stream_object()
so that there is no confusion between write_to_file() and
write_bits_to_fileobject().  For backward compatibility,
write_bits_to_fileobject() will continue to work if you are
writing a bitvector to a string stream object.

The class is provided with the following operators/methods:

-      __getitem__
-      __setitem__
-      __len__
-      __iter__
-      __contains__
-      __str__
-      __int__
-      __add__
-      __eq__, __ne__, __lt__, __le__, __gt__, __ge__
-      __or__
-      __and__
-      __xor__
-      __invert__
-      __lshift__
-      __rshift__
-      __add__
-      close_file_object
-      count_bits 
-      count_bits_sparse      (faster for sparse bit vectors)     
-      deep_copy
-      divide_into_two
-      gcd                    (for greatest common divisor)
-      gen_random_bits 
-      get_bitvector_in_ascii
-      get_bitvector_in_hex
-      gf_divide_by_modulus   (for modular divisions in GF(2^n))
-      gf_MI                  (for multiplicative inverse in GF(2^n))
-      gf_multiply            (for multiplications in GF(2))
-      gf_multiply_modular    (for multiplications in GF(2^n))
-      hamming_distance
-      int_val                (for returning the integer value) 
-      is_power_of_2
-      is_power_of_2_sparse   (faster for sparse bit vectors)
-      jaccard_distance
-      jaccard_similarity
-      length                 
-      min_canonical
-      multiplicative_inverse
-      next_set_bit
-      pad_from_left
-      pad_from_right
-      permute
-      rank_of_bit_set_at_index
-      read_bits_from_file
-      reset
-      reverse
-      runs
-      set_value
-      shift_left             (for non-circular left shift)
-      shift_right            (for non-circular right shift)
-      test_for_primality
-      unpermute
-      write_to_file
-      write_bits_to_stream_object

          ''',
      license='Python Software Foundation License',
      keywords='bit array, bit vector, bit string, logical operations on bit fields',
      platforms='All platforms',
      classifiers=['Topic :: Utilities', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.5'],
      packages=['BitVector']
)
