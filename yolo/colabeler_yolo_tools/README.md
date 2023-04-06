# colabeler_yolo_tools

* Download Colabeler(精灵标注助手) please visit http://www.jinglingbiaozhu.com/

* Prerequisite：

  ```
  pip install opencv-python
  ```
  Make sure all pictures are jpg, use [jpg_conversion.py](./jpg_conversion.py) if needed.
* To change object type...
 
  Edit index in both [colabeler2yolo.py](./colabeler2yolo.py) and [yolo2colabeler.py](./yolo2colabeler.py)

  ```python
  # colabeler2yolo.py
  index = {'Object0':0,'Object1':1,'Object2':2,'Object3':3,'Object4':4,'Object5':5,'Object6':6,'Object7':7}

  # yolo2colabeler.py
  index = {0:"object0",1:"object1",2:"object2",3:"object3",4:"object4",5:"object5",6:"object6",7:"object7"}
  ```

## [colabeler2yolo.py](./colabeler2yolo.py)
* picture folder, xml folder, yolo txt destination folder(optional)
  ```
  python colabeler2yolo.py ./pic ./outputs ./outputs_yolo
  ```

## [yolo2colabeler.py](./yolo2colabeler.py)
* picture folder, yolo txt folder, xml destination folder(optional)

  ```
  python yolo2colabeler.py ./pic ./outputs_yolo ./outputs_xml
  ```

