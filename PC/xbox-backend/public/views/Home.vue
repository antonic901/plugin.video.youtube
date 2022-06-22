<template>
    <div>
        <v-row dense no-gutters>
            <v-col align="center">
                <a style="color: green;" href="https://api.invidious.io">Click here to see available Invidious Instances</a>
            </v-col>
        </v-row>
        <v-row align="center"  align-self="center" dense no-gutters>
            <v-spacer></v-spacer>
            <v-col cols="12" sm="10">
                <v-text-field color="green" class="mb-1" v-model="provider" label="Enter url for Invidious API" hint="ex: https://name_of_api"></v-text-field>
            </v-col>
            <v-col cols="12" sm="2" align="center" align-self="center">
                 <v-btn class="mb-3" v-on:click="test" :disabled="provider == null || provider == ''" color="success">Test</v-btn>
            </v-col>
            <v-spacer></v-spacer>
        </v-row>
        <div v-if="status">
            <v-card class="my-5" flat>
                <v-row>
                    <v-col align="center">
                        API status:<span class="ml-1" style="color:green">Online</span>
                    </v-col> 
                </v-row>
                <v-card-text>
                    <v-row no-gutters align="center" class="ml-2 grey--text font-weight-black">
                        <v-col>
                            <span>Software</span>
                        </v-col>
                    </v-row>
                    <v-divider></v-divider>
                    <v-row class="px-2" no gutters>
                        <v-col align="start">
                            Name: <span>{{status.software.name}}</span>
                        </v-col>
                        <v-col align="center">
                            Branch: <span>{{status.software.branch}}</span>
                        </v-col>
                        <v-col align="end">
                            Version: <span>{{status.software.version}}</span>
                        </v-col>
                    </v-row>
                    <v-row no-gutters align="center" class="ml-2 mt-2 grey--text font-weight-black">
                        <v-col>
                            <span>Usage</span>
                        </v-col>
                    </v-row>
                    <v-divider></v-divider>
                    <v-row class="px-2" no gutters>
                        <v-col align="start">
                            Total: <span>{{status.usage.users.total}}</span>
                        </v-col>
                        <v-col align="center">
                            Active per half year: <span>{{status.usage.users.activeHalfyear}}</span>
                        </v-col>
                        <v-col align="end">
                            Active per month: <span>{{status.usage.users.activeMonth}}</span>
                        </v-col>
                    </v-row>
                    <v-row no-gutters align="center" class="ml-2 mt-2 grey--text font-weight-black">
                        <v-col>
                            <span>Metadata</span>
                        </v-col>
                    </v-row>
                    <v-divider></v-divider>
                    <v-row class="px-2" no gutters>
                        <v-col align="start">
                            Channel refreshed at: <span>{{getDateAndTime(status.metadata.lastChannelRefreshedAt * 1000)}}</span>
                        </v-col>
                        <v-col align="end">
                            API updated at: <span>{{getDateAndTime(status.metadata.updatedAt * 1000)}}</span>
                        </v-col>
                    </v-row>
                    <v-row class="px-2">
                        <v-col aling="start">
                            Login: {{status.openRegistrations ? 'Available' : 'Not Available'}}
                        </v-col>
                        <v-col align="end">
                            Version: {{status.version}}
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
            <v-row>
                <v-spacer></v-spacer>
                <v-btn v-on:click="updateApi" color="success">Update API</v-btn>
                <v-spacer></v-spacer>
            </v-row>
        </div>
        <div v-if="usedProvider">
            <v-row class="mt-6" no-gutters>
                Status of current used API ({{usedProvider.providerName}}):
            </v-row>
            <v-card class="my-5" flat>
                <v-row>
                    <v-col align="center">
                        API status:<span class="ml-1" style="color:green">Online</span>
                    </v-col> 
                </v-row>
                <v-card-text>
                    <v-row no-gutters align="center" class="ml-2 grey--text font-weight-black">
                        <v-col>
                            <span>Software</span>
                        </v-col>
                    </v-row>
                    <v-divider></v-divider>
                    <v-row class="px-2" no gutters>
                        <v-col align="start">
                            Name: <span>{{usedProvider.software.name}}</span>
                        </v-col>
                        <v-col align="center">
                            Branch: <span>{{usedProvider.software.branch}}</span>
                        </v-col>
                        <v-col align="end">
                            Version: <span>{{usedProvider.software.version}}</span>
                        </v-col>
                    </v-row>
                    <v-row no-gutters align="center" class="ml-2 mt-2 grey--text font-weight-black">
                        <v-col>
                            <span>Usage</span>
                        </v-col>
                    </v-row>
                    <v-divider></v-divider>
                    <v-row class="px-2" no gutters>
                        <v-col align="start">
                            Total: <span>{{usedProvider.usage.users.total}}</span>
                        </v-col>
                        <v-col align="center">
                            Active per half year: <span>{{usedProvider.usage.users.activeHalfyear}}</span>
                        </v-col>
                        <v-col align="end">
                            Active per month: <span>{{usedProvider.usage.users.activeMonth}}</span>
                        </v-col>
                    </v-row>
                    <v-row no-gutters align="center" class="ml-2 mt-2 grey--text font-weight-black">
                        <v-col>
                            <span>Metadata</span>
                        </v-col>
                    </v-row>
                    <v-divider></v-divider>
                    <v-row class="px-2" no gutters>
                        <v-col align="start">
                            Channel refreshed at: <span>{{getDateAndTime(usedProvider.metadata.lastChannelRefreshedAt * 1000)}}</span>
                        </v-col>
                        <v-col align="end">
                            API updated at: <span>{{getDateAndTime(usedProvider.metadata.updatedAt * 1000)}}</span>
                        </v-col>
                    </v-row>
                    <v-row class="px-2">
                        <v-col aling="start">
                            Login: {{usedProvider.openRegistrations ? 'Available' : 'Not Available'}}
                        </v-col>
                        <v-col align="end">
                            Version: {{usedProvider.version}}
                        </v-col>
                    </v-row>
                </v-card-text>
            </v-card>
        </div>
        <div class="color:red;" v-else>Current used API seems to be offline at this moment.</div>
        <BasicNotification v-bind:show-notification="showNotification" v-bind:text="message" v-on:close="showNotification=false, message=''"></BasicNotification>
    </div>
</template>

<script>
module.exports = {
    name: 'Home',
    data () {
        return {
            provider: '',
            usedProvider: null,
            showNotification: false,
            message: '',
            status: null
        }
    },
    methods: {
        test() {
            axios.post("/test", {link: this.provider})
                .then(r => {
                    this.status = r.data;
                })
                .catch(e => {
                    this.message = e.response.data;
                    this.showNotification = true;
                })
        },
        updateApi() {
            axios.put("/update-api", {api: this.provider})
                .then(() => {
                    this.message = 'Successsfully updated API.';
                    this.showNotification = true;
                    this.usedProvider = this.status;
                    this.provider = '';
                    this.status = null;
                })
                .catch(() => {
                    this.message = 'Something went wrong.';
                    this.showNotification = true;
                })
        },
        getDateAndTime(milliseconds) {
            let date = new Date(milliseconds);
            return date.toLocaleString('en-US');
        }
    },
    created() {
        axios.get("/api/v1/stats")
            .then(r => {
                this.usedProvider = r.data;
            })
            .catch(e => {
                this.message = 'Can not get info about current provider. Maybe its offline?'
                this.showNotification = true;
            })
    }
}
</script>