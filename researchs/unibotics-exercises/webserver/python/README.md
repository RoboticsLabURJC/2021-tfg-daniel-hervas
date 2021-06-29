# Unibotics Exercises

This directory contains Unibotics exercises. Each subfolder must contain some files in order to remove the prefix `working_`.

Check that the exercise contains:

- Files needed to **run the exercise**.
- **Theory** in MarkDown format
- Reference **solution**.
- .**json** with exercise information (see example).

`.json`example:
```
{
  "exercise_id":{
    "language": "python",
    "platform": "gazebo",
    "world": ".world",
    "models": "",
    "referee": false
  }
}
```