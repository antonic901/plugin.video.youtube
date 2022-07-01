<template>
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
</template>

<script>
module.exports = {
    name: 'ProviderStatus',
    props: {
        status: Object
    },
    methods: {
        getDateAndTime(milliseconds) {
            let date = new Date(milliseconds);
            return date.toLocaleString('en-US');
        }
    }
}
</script>