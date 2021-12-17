import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='root2mpl',
    version='0.1.0',
    description='Python module for converting ROOT histograms and graphs into Matplotlib-compatible objects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/JacksonPybus/root2mpl',
    author='Jackson Pybus',
    author_email='jrpybus@mit.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Scientific/Engineering',
        'Framework :: Matplotlib',
        ],
    py_modules=["root2mpl"],
    python_requires='>=3.7',
    install_requires=['numpy',
                      'matplotlib',
                      ]
)
