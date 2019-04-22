//
//  StatusMenuController.swift
//  MCUClient
//
//  Created by Anatoly Kasyanov on 2/14/19.
//

import Foundation
import Cocoa

class StatusMenuController: NSObject {
    
    enum door: String {
        case Open = "Open"
        case Closed = "Closed"
    }
    
    let status = StatusAPI()
    
    let isOpen = true
    
    @IBOutlet weak var menu: NSMenu!
    
    override init() {
        super.init()
        Timer.scheduledTimer(timeInterval: 2.0, target: self, selector: #selector(updateStatus), userInfo: nil, repeats: true)
    }
    
    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
    
    @IBAction func updateClicked(_ sender: NSMenuItem) {
        updateStatus()
    }
    
    @objc func updateStatus() {
//        self.statusItem.button?.image = NSImage(named:NSImage.Name("statusIconOccupied"))
        status.makeGetCall { success in
            DispatchQueue.main.async {
                if success == "false" {
                    self.statusItem.button?.image = NSImage(named:NSImage.Name("statusIconOccupied"))
                }
                if success == "true" {
                    self.statusItem.button?.image = NSImage(named:NSImage.Name("statusIconFree"))
                }
                if success == "noConnection" {
                    self.statusItem.button?.image = NSImage(named:NSImage.Name("statusIconBlackTheme"))
                }
            }
        }
    }
    
    @IBAction func quitClicked(sender: NSMenuItem) {
        NSApplication.shared.terminate(self)
    }
}
