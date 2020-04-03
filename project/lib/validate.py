def val_empty_str(data):

  #print("1-->", data)
  emp = data[0]
  #print("1****", emp)
  if len(emp) > 0:
    #print("===here===", ['']+data)
    return ([''] + data)
  return data

def val_time(data):
  #print("2-->", data)

  time = data[1]
  if len(time) <= 13:
    return data
  else:
    return (data[0:1] + [""] + data[1:])

def val_room_num(data):
  #print("3-->", data)
  room_num = data[4]
  if len(room_num) <=8:
    return data
  else:
    return (data[0:4] + [""] + data[4:])


def validate(data):
  data = val_empty_str(data)
  data = val_time(data)
  data = val_room_num(data)

  #print("4-->", data)
  return data

