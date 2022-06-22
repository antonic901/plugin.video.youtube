<template>
    <v-snackbar top rounded="lg" transition="slide-y-transition" v-model="show" timeout="5000" color="white" elevation="6">
    <span class="grey--text font-weight-medium">{{text}}</span>
    <template v-slot:action="{ attrs }">
        <v-btn color="red" icon text v-bind="attrs" v-on:click="close()"><v-icon>mdi-close-thick</v-icon></v-btn>
    </template>
    </v-snackbar>
</template>

<script>
module.exports = {
    name: 'BasicNotification',
    props: {
        showNotification: Boolean,
        text: String
    },
    computed: {
      show: {
        get() {
          return this.showNotification;
        },
        set(showNotification) {
          this.$emit('close', showNotification);
        }
      }
    },
    methods: {
        close() {
            this.$emit('close')
        }
    }
}
</script>