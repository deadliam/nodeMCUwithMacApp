//
//  StatusMenuController.swift
//  MCUClient
//
//  Created by Anatoly Kasyanov on 2/14/19.
//

import Foundation
import Cocoa

class StatusMenuController: NSObject, NSMenuItemValidation {
    
    var songsArray = ["closed",
    "supermario",
    "Super Mario - Title Music",
    "SMBtheme",
    "SMBwater",
    "SMBunderground",
    "The Simpsons",
    "Indiana",
    "TakeOnMe",
    "Cantina",
    "Entertainer",
    "McGyver",
    "StarWars",
    "TopGun",
    "A-Team",
    "Smurfs",
    "starwars2",
    "ImperialMarch",
    "ItchyScratchy",
    "MissionImp",
    "forest",
    "1up"]
    
    enum songs: String {
        case superMario = "supermario"
        case superMario2 = "Super Mario - Title Music"
        case superMarioTheme = "SMBtheme"
        case superMarioWater = "SMBwater"
        case superMarioUnderground = "SMBunderground"
        case theSimpsons = "The Simpsons"
        case indiana = "Indiana"
        case takeOnMe = "TakeOnMe"
        case cantina = "Cantina"
        case entertainer = "Entertainer"
        case mcGyver = "McGyver"
        case starWars = "StarWars"
        case topGun = "TopGun"
        case aTeam = "A-Team"
        case smurfs = "Smurfs"
        case starwars2 = "starwars2"
        case imperialMarch = "ImperialMarch"
        case itchyScratchy = "ItchyScratchy"
        case missionImpossible = "MissionImp"
        case forest = "forest"
        case oneUp = "1up"
        case closed = "closed"
    }
    
    var song: String?
    
    let status = StatusAPI()
    
    override init() {
        super.init()
        Timer.scheduledTimer(timeInterval: 10.0, target: self, selector: #selector(updateStatus), userInfo: nil, repeats: true)
    }
    
    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
    
    
//    @IBAction func updateClicked(_ sender: NSMenuItem) {
//        updateStatus()
//    }
    
    @objc func updateStatus() {
        song = status.readConfig()
        if song == "" && !songsArray.contains(song!) {
            song = songs.closed.rawValue
        }
        constructMenu()
        status.makeGetCall { success in
            DispatchQueue.main.async {
                
                if success == "false" {
                    self.statusItem.button?.image = NSImage(named:NSImage.Name("statusIconOccupied"))
                }
                if success == "true" {
                    self.statusItem.button?.image = NSImage(named:NSImage.Name("statusIconFree"))
                }
                if success == "noConnection" {
                    self.statusItem.button?.image = NSImage(named:NSImage.Name("statusIconDarkTheme"))
//                    self.statusItem.isEnabled = false
                }
            }
        }
    }
    
    func validateMenuItem(_ menuItem: NSMenuItem) -> Bool {
        return true
    }
    
    func constructMenu() {
        let menu = NSMenu()
        let getOutItem = NSMenuItem(title: "Get out!", action: #selector(sendSignalToServer(_:)), keyEquivalent: "g")
        getOutItem.target = self
        menu.addItem(getOutItem)
        
//        if value == "volts" {
//            let voltsItem = NSMenuItem(title: value, action: nil, keyEquivalent: "")
//            voltsItem.target = self
//            menu.addItem(voltsItem)
//        }
        menu.addItem(NSMenuItem.separator())
        let quitItem = NSMenuItem(title: "Quit", action: #selector(quitClicked(_:)), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)
        statusItem.menu = menu
    
    }
    
    @objc func sendSignalToServer(_ sender: Any?) {
        status.makePostRequest(song: song!)
    }
    
    @IBAction func quitClicked(_ sender: NSMenuItem) {
        NSApplication.shared.terminate(self)
    }
}
