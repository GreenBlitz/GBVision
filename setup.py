from setuptools import setup

setup(
    name='gbvision',
    version='0.7.7',
    description='A Python Vision Library for object tracking in the 3D physical space',
    license='Apache License 2.0',
    packages=['gbvision',
              'gbvision/utils',
              'gbvision/utils/net',
              'gbvision/constants',
              'gbvision/exceptions',
              'gbvision/utils/finders',
              'gbvision/gui',
              'gbvision/models',
              'gbvision/tools',
              'gbvision/utils/continuity',
              'gbvision/utils/cameras',
              'gbvision/utils/thresholds',
              'gbvision/utils/shapes',
              'gbvision/utils/recorders',
              'gbvision/utils/denoising'],
    author='Ido Heinemann',
    author_email='idohaineman@gmail.com',
    keywords=['computer vision', 'frc', 'first', 'image processing'],
    url='https://github.com/GreenBlitz/GBVision',
    download_url='https://github.com/GreenBlitz/GBVision/archive/v0.7.7-beta.tar.gz',
    install_requires=[
        'numpy',
        'opencv-python',
        'opencv-contrib-python',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

        'Intended Audience :: Developers',  # Define that your audience are developers

        'Programming Language :: Python :: 3',  # Specify which python versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
