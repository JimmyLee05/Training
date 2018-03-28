//
//  FitModel.swift
//  myForm
//
//  Created by bb on 2017/6/2.
//  Copyright © 2017年 bb. All rights reserved.
//

import UIKit

class FitModel: NSObject {

    fileprivate let audio = Audio.shared

    static let shared = FitModel()

    static var recentTimeArray: [TimeInterval] = []

    ///配速 格式化方法
    ///参数：当前配速（单位：米/秒）
    ///返回值：字典  类型：字典
    func dictionaryFromTimePace(pace: Float) -> Dictionary<String, String>{
        if pace == 0 {
            return ["min":"-", "sec":"-"]
        } else {
            let minutes = Int(pace)
            let str = String(format: "%.2f", pace)
            let range = str.range(of: ".")
            let seconds = String(str[(range?.upperBound)!])
            return ["m":"\(minutes)", "s":"\(seconds)"]
        }
    }

    ///已用时间 格式化方法
    ///参数：当前用时（单位：毫秒）
    ///返回值：字典  类型：字典
    func dictionaryFromTimeInterval(interval: Double) -> Dictionary<String, Int> {
        let interval = Int(interval)
        let seconds = interval % 60
        let minutes = interval / 60
        let hours = interval / 3600
        return ["h": hours,"m": minutes, "s": seconds]
    }

    ///跑步状态-语音播报方法
    ///参数：当前运动状态（类型：字符串）
    ///返回值：无  类型：无
    func reportStatus(status: String){
        var array:[String] = []
        switch status {
        case "start":
            array = ["N001", "N002", "N003", "Eg_9_go"]
            break
        case "pause":
            array = ["Rpause"]
            break
        case "keep":
            array = ["Rresume"]
            break
        case "stop":
            array = ["Rcomplete"]
            break
        default:
            break
        }
        guard !array.isEmpty else {
            return
        }
        audio.arrayOfTracks = array
    }

    ///路程-语音播报方法
    ///参数1：当前路程（单位：公里）
    ///参数2：所用时间（单位：秒）
    ///返回值：无  类型：无
    func reportDistance(distance: Int, time: TimeInterval) {
        //distance 可能值为 0/1/2/3/4/5/6... 整型数
        guard distance > 0 else {
            return
        }
        //小于2公里
        if distance < 2 {
            //拓展GDC once，当distance改变时才执行
            DispatchQueue.once(token: String(distance)) {
                //所有需要依次播报的音轨名称
                var array:[String] = []
                let t = dictionaryFromTimeInterval(interval: time)
                FitModel.recentTimeArray.append(time)
                switch time {
                case 0..<60:
                    array = ["Rprompt", "Rrunned_distance", "N000", "Rkm", "Rtimecost", "N000", "Rseconds"]
                    //获取秒数音轨
                    let secondsStr = FitModel.getTrackName(number: t["s"]!)
                    if secondsStr != ""{
                        array[5] = secondsStr
                    }
                    break
                case 60..<3600:
                    array = ["Rprompt", "Rrunned_distance", "N000", "Rkm", "Rtimecost", "N000", "Rminutes", "N000", "Rseconds"]
                    //获取分钟数音轨
                    let minutesStr = FitModel.getTrackName(number: t["m"]!)
                    if minutesStr != ""{
                        array[5] = minutesStr
                    }
                    //获取秒数音轨
                    let secondsStr = FitModel.getTrackName(number: t["s"]!)
                    if secondsStr != ""{
                        array[7] = secondsStr
                    }
                    break
                default:
                    array = ["Rprompt", "Rrunned_distance", "N000", "Rkm", "Rtimecost", "N000", "Rhours", "N000", "Rminutes", "N000", "Rseconds"]
                    //获取小时音轨
                    let hoursStr = FitModel.getTrackName(number: t["h"]!)
                    if hoursStr != ""{
                        array[5] = hoursStr
                    }
                    //获取分钟数音轨
                    let minutesStr = FitModel.getTrackName(number: t["m"]!)
                    if minutesStr != ""{
                        array[7] = minutesStr
                    }
                    //获取秒数音轨
                    let secondsStr = FitModel.getTrackName(number: t["s"]!)
                    if secondsStr != ""{
                        array[9] = secondsStr
                    }
                    break
                }
                //获取公里数音轨
                let distanceStr = FitModel.getTrackName(number: distance)
                // 在121公里之后，distanceStr可能存在空值
                guard distanceStr != "" else{
                    return
                }
                array[2] = distanceStr
                audio.arrayOfTracks = array
            }
        } else {
            //拓展GDC once，当distance改变时才执行
            DispatchQueue.once(token: String(distance)) {
                //所有需要依次播报的音轨名称
                var array:[String] = []
                FitModel.recentTimeArray.append(time)
                let recent = FitModel.recentTimeArray[FitModel.recentTimeArray.count - 2]
                let t = dictionaryFromTimeInterval(interval: time)
                let r = dictionaryFromTimeInterval(interval: time - recent)
                switch time {
                case 0..<60:
                    array = ["Rprompt", "Rrunned_distance", "N000", "Rkm", "Rtimecost", "N000",  "Rseconds", "Rrecent_1km_timecost", "N000", "Rseconds", "Rcheer2"]
                    //获取秒数音轨
                    let secondsStr = FitModel.getTrackName(number: t["s"]!)
                    if secondsStr != ""{
                        array[5] = secondsStr
                    }

                    //获取前1公里秒数音轨
                    let recentSecondsStr = FitModel.getTrackName(number: r["s"]!)
                    if recentSecondsStr != ""{
                        array[8] = recentSecondsStr
                    }
                    break
                case 60..<3600:
                    array = ["Rprompt", "Rrunned_distance", "N000", "Rkm", "Rtimecost", "N000", "Rminutes", "N000", "Rseconds", "Rrecent_1km_timecost", "N000", "Rminutes", "N000", "Rseconds", "Rcheer2"]
                    //获取分钟数音轨
                    let minutesStr = FitModel.getTrackName(number: t["m"]!)
                    if minutesStr != ""{
                        array[5] = minutesStr
                    }
                    //获取秒数音轨
                    let secondsStr = FitModel.getTrackName(number: t["s"]!)
                    if secondsStr != ""{
                        array[7] = secondsStr
                    }

                    //获取前1公里分钟数音轨
                    let recentMinutesStr = FitModel.getTrackName(number: r["m"]!)
                    if recentMinutesStr != ""{
                        array[10] = recentMinutesStr
                    }
                    //获取前1公里秒数音轨
                    let recentSecondsStr = FitModel.getTrackName(number: r["s"]!)
                    if recentSecondsStr != ""{
                        array[12] = recentSecondsStr
                    }
                    break
                default:
                    array = ["Rprompt", "Rrunned_distance", "N000", "Rkm", "Rtimecost", "N000", "Rhours", "N000", "Rminutes", "N000", "Rseconds", "Rrecent_1km_timecost", "N000", "Rhours", "N000", "Rminutes", "N000", "Rseconds", "Rcheer2"]
                    //获取小时音轨
                    let hoursStr = FitModel.getTrackName(number: t["h"]!)
                    if hoursStr != ""{
                        array[5] = hoursStr
                    }
                    //获取分钟数音轨
                    let minutesStr = FitModel.getTrackName(number: t["m"]!)
                    if minutesStr != ""{
                        array[7] = minutesStr
                    }
                    //获取秒数音轨
                    let secondsStr = FitModel.getTrackName(number: t["s"]!)
                    if secondsStr != ""{
                        array[9] = secondsStr
                    }

                    //获取前1公里小时音轨
                    let recentHoursStr = FitModel.getTrackName(number: r["h"]!)
                    if recentHoursStr != ""{
                        array[12] = recentHoursStr
                    }
                    //获取前1公里分钟数音轨
                    let recentMinutesStr = FitModel.getTrackName(number: r["m"]!)
                    if recentMinutesStr != ""{
                        array[14] = recentMinutesStr
                    }
                    //获取前1公里秒数音轨
                    let recentSecondsStr = FitModel.getTrackName(number: r["s"]!)
                    if recentSecondsStr != ""{
                        array[16] = recentSecondsStr
                    }
                    break
                }
                //获取公里数音轨
                let distanceStr = FitModel.getTrackName(number: distance)
                // 在121公里之后，distanceStr可能存在空值
                guard distanceStr != "" else{
                    return
                }
                if distance == 2{
                    array[2] = "N002_3"
                }else{
                    array[2] = distanceStr
                }
                audio.arrayOfTracks = array
            }
        }
    }

    ///根据路程返回不同的语音文件名
    ///参数：当前路程（单位：公里）
    ///返回值：语音播报的对应的.mp3文件 类型：字符串
    class func getTrackName(number: Int) -> String {

        var str = ""
        switch number {
        case 0...9:
            str = "N00\(number)"
            break
        case 10...99:
            str = "N0\(number)"
            break
        case 100...120:
            str = "N\(number)"
            break
        case 130:
            str = "N130"
            break
        case 140:
            str = "N140"
            break
        case 150:
            str = "N150"
            break
        case 160:
            str = "N160"
            break
        case 200:
            str = "N200"
            break
        case 300:
            str = "N300"
            break
        case 400:
            str = "N400"
            break
        case 500:
            str = "N500"
            break
        case 600:
            str = "N600"
            break
        case 700:
            str = "N700"
            break
        case 800:
            str = "N800"
            break
        case 900:
            str = "N900"
            break
        default:
            str = "Eblank"
            break
        }
        return str
    }
}

