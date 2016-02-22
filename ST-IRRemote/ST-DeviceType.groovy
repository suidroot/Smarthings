/**
 *  IR Remote control for Smartthign shield
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
metadata {
	definition (name: "Remote Control", namespace: "suidroot", author: "Ben Mason") {
        capability "Refresh"

		//attribute "tvpower", "string"

		command "sendtvpower"
		command "sendapautosleep"
		command "sendapauto"

	}

	// Simulator metadata
	simulator {
		status "on":  "catchall: 0104 0000 01 01 0040 00 0A21 00 00 0000 0A 00 0A6F6E"
		status "off": "catchall: 0104 0000 01 01 0040 00 0A21 00 00 0000 0A 00 0A6F6666"

		// reply messages
		reply "raw 0x0 { 00 00 0a 0a 6f 6e }": "catchall: 0104 0000 01 01 0040 00 0A21 00 00 0000 0A 00 0A6F6E"
		reply "raw 0x0 { 00 00 0a 0a 6f 66 66 }": "catchall: 0104 0000 01 01 0040 00 0A21 00 00 0000 0A 00 0A6F6666"

		status "ping": "catchall: 0104 0000 01 01 0040 00 6A67 00 00 0000 0A 00 0A70696E67"
		status "response": "catchall: 0104 0000 01 01 0040 00 0A21 00 00 0000 0A 00 0A4F4D4E4F4D4E4F4D4E4F4D"
	}

	// UI tile definitions
	tiles {
		
		standardTile("tvpower", "device.sheild", width: 1, height: 1, canChangeIcon: false) {
			state "off", label: 'TV Power', action: "sendtvpower", icon: "st.switches.switch.off", backgroundColor: "#ffffff", nextState: "on"
			state "on", label: 'TV Power', action: "sendtvpower", icon: "st.switches.switch.on", backgroundColor: "#53a7c0", nextState: "off"
		}

		standardTile("airpurifierautosleep", "device.sheild", width: 1, height: 1, canChangeIcon: false) {
			state "off", label: 'AP Auto Sleep', action: "sendapautosleep", icon: "st.switches.switch.off", backgroundColor: "#ffffff", nextState: "on"
			state "on", label: 'AP Auto Sleep', action: "sendapautosleep", icon: "st.switches.switch.on", backgroundColor: "#53a7c0", nextState: "off"
		}

		standardTile("airpurifierauto", "device.sheild", width: 1, height: 1, canChangeIcon: false) {
			state "off", label: 'AP Auto', action: "sendapauto", icon: "st.switches.switch.off", backgroundColor: "#ffffff", nextState: "on"
			state "on", label: 'AP Auto', action: "sendapauto", icon: "st.switches.switch.on", backgroundColor: "#53a7c0", nextState: "off"
		}

		standardTile("airpurifierturbo", "device.sheild", width: 1, height: 1, canChangeIcon: false) {
			state "off", label: 'AP Turbo', action: "sendapturbo", icon: "st.switches.switch.off", backgroundColor: "#ffffff", nextState: "on"
			state "on", label: 'AP Turbo', action: "sendapturbo", icon: "st.switches.switch.on", backgroundColor: "#53a7c0", nextState: "off"
		}

		/*standardTile("refresh", "device.status", inactiveLabel: false, decoration: "flat") {
        	state "default", label:"", action:"refresh.refresh", icon:"st.secondary.refresh", backgroundColor:"#ffffff"
    	} */


		main("tvpower", "airpurifierautosleep", "airpurifierauto","airpurifierturbo")
		details("tvpower", "airpurifierautosleep", "airpurifierauto","airpurifierturbo")

	}
}

// Parse incoming device messages to generate events
def parse(String description) {

	def value = zigbee.parse(description)?.text
	def name = value && value != "ping" ? "response" : null
	def result = createEvent(name: name, value: value)
	log.debug "Parse returned ${result?.descriptionText}"
	return result
}


/*
 * NEC: 61A0F00F tv power
 * NEC: 48B710EF auto sleep
 * NEC: 48B7609F  auto
 * NEC: 77E1505B apple tv up
 */

// Commands sent to the device
def sendtvpower() {
	zigbee.smartShield(text: "61A0F00F").format()
}

def sendapautosleep() {
	zigbee.smartShield(text: "48B710EF").format()
}

def sendapauto() {
	zigbee.smartShield(text: "48B7609F").format()
}

def sendapturbo() {
	zigbee.smartShield(text: "48B76897").format()
}