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
            <ProviderStatus v-bind:status="status"></ProviderStatus>
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
            <ProviderStatus v-bind:status="usedProvider"></ProviderStatus>
        </div>
        <div v-else>Current used API seems to be offline at this moment.</div>
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
                    this.usedProvider.providerName = this.provider;
                    this.provider = '';
                    this.status = null;
                })
                .catch(() => {
                    this.message = 'Something went wrong.';
                    this.showNotification = true;
                })
        }
    },
    created() {
        axios.get("/api/v1/stats")
            .then(r => {
                this.usedProvider = r.data;
            })
            .catch(e => {
                this.message = 'Can not get info about ' + e.response.data.providerName + ' provider. Maybe its offline?'
                this.showNotification = true;
            })
    }
}
</script>