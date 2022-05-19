from datetime import datetime
class Attendance():
    def markAttendance(self, names):
        with open('attendance.csv', 'r+') as f:
            dataList = f.readlines()
            nameList = []
            for line in dataList:
                entry = line.split(',')
                nameList.append(entry[0])
            for name in names:
                if name not in nameList:
                    now = datetime.now()
                    dateString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dateString}')